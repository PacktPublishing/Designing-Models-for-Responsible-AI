The first step is to clone the hashicorp/vault-guides repository from GitHub

git clone https://github.com/hashicorp/vault-guides.git

The next step is to navigate inside vault-guides/identity/vault-agent-k8s-demo directory.

cd vault-guides/identity/vault-agent-k8s-demo

Next, we start a Vault dev server which listens for requests locally at 0.0.0.0:8200 with root as the root token ID.

vault server -dev -dev-root-token-id root -dev-listen-address 0.0.0.0:8200

To provide an URL access, export an environment variable for the vault CLI to address the Vault server

export VAULT\_ADDR=http://0.0.0.0:8200

To create a service account we can start a Kubernetes cluster running in Minikube

minikube start --driver=docker

Check the status of the minikube environment if its fully available

minikube status

The output from the status will be displayed as:

host: Running

kubelet: Running

apiserver: Running

kubeconfig: Configured

After verifying the status, we examine the contents of vault-auth-service-account.yaml for service account creation

Next we create a Kubernetes service account named vault-auth.

kubectl create serviceaccount vault-auth

Update the vault-auth service account

kubectl apply --filename vault-auth-service-account.yaml

Now to configure Kubernetes auth method, we create a read-only policy, myapp-kv-ro in Vault

vault policy write myapp-kv-ro - <<EOF

path "secret/data/myapp/\*" {

capabilities = ["read", "list"]

}

EOF

In the following step, we create some test data at the secret/myapp path

vault kv put secret/myapp/config \

username='appuser' \

password='suP3rsec(et!' \

ttl='30s'

Now let us set the environment variables to point to the running Minikube environment. Here we set the VAULT\_SA\_NAME environment variable value to the vault-auth service account.

export VAULT\_SA\_NAME=$(kubectl get sa vault-auth \

--output jsonpath="{.secrets[\*]['name']}")

Here, we also set the SA\_JWT\_TOKEN environment variable value to the service account JWT used to access the TokenReview API.

export SA\_JWT\_TOKEN=$(kubectl get secret $VAULT\_SA\_NAME \

--output 'go-template={{ .data.token }}' | base64 --decode)

Next, we set the SA\_CA\_CRT environment variable value to the PEM encoded CA cert used to talk to Kubernetes API.

export SA\_CA\_CRT=$(kubectl config view --raw --minify --flatten \

--output 'jsonpath={.clusters[].cluster.certificate-authority-data}' | base64 --decode)

Now the minikube IP address should be available, hence we point the K8S\_HOST environment variable value to this.

export K8S\_HOST=$(kubectl config view --raw --minify --flatten \

--output 'jsonpath={.clusters[].cluster.server}')

Finally, we need to enable and configure the Kubernetes auth method at the default path ("auth/kubernetes").

vault auth enable kubernetes

Further, we also let Vault how to communicate with the Kubernetes (Minikube) cluster.

vault write auth/kubernetes/config \

token\_reviewer\_jwt="$SA\_JWT\_TOKEN" \

kubernetes\_host="$K8S\_HOST" \

kubernetes\_ca\_cert="$SA\_CA\_CRT" \

issuer="https://kubernetes.default.svc.cluster.local"

Having configured all at last we need to create a role named, example, that maps the Kubernetes Service Account to Vault policies and default token TTL.

vault write auth/kubernetes/role/example \

bound\_service\_account\_names=vault-auth \

bound\_service\_account\_namespaces=default \

policies=myapp-kv-ro \

ttl=24h
