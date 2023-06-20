# Kubernets
check test-k8s repository

source (chinese)
1. https://k8s.easydoc.net/docs/dRiQjyTY/28366845/6GiNOzyZ/puf7fjYr
2. https://www.bilibili.com/video/BV1Tg411P7EB?p=3&vd_source=becc7aaed81e7e83a9c5094649aae42d

* Pod K8s最小單位
* 可包含1-多個container
* 每個pod自己的虛擬id
* minikube只有一個node, 若有多個master不跑pod

addition
* check what is in the backgroud `bg` -> access bg process `fg %{id}`
* current running process `ps aux | grep "kubectl port-forward"`, `kill -9 {id}`

## setup minikube
* 加結點 `minikube node add [--worker]`
* start service `minikube start`

## run app
1. command line `kubectl run {appname} --image={image}`
2. pod yaml file `kubectl apply -f yaml/deployment/pod.yaml`
3. deployment yaml file (multiple pod) `kubectl apply -f yaml/deployment/deployment.yaml`
4. kubectl delete deployment {name}

## check status
1. `kubectl get pod (-o wide)` (-o wide check ip, node info)
2. see details like "events" `kubectl describe pod/ {pod id}`
3.  `kubectl logs {pod id} (-f)`: -f non stop log
4. `kubectl get deployment`

## manage deployment
1. Scale up / down with cmd: `kubectl scale deployment test-k8s --replicas=3`, can also change in the file and reapply
2. 進到容器裡 `kubectl exec -it {pod id} -- bash` `(-c {container id})` 指定容器
3. 訪問pod `kubectl port-forward {pod id} 8080:8080` first 8080 local, 2nd pod port

## check history

* `kubectl rollout history deployment test-k8s`
* roll back `test_k8s kubectl rollout undo deployment k8s`
* specify version `kubectl rollout undo deployment test-k8s --to-revision=2`

## Other command

* 查看全部 `kubectl get all`
* 重新部署 `kubectl rollout restart deployment test-k8s`
* 命令修改镜像，--record 表示把这个命令记录到操作历史中
```
kubectl set image deployment test-k8s test-k8s=ccr.ccs.tencentyun.com/k8s-tutorial/test-k8s:v2-with-error --record
```
* 暂停运行，暂停后，对 deployment 的修改不会立刻生效，恢复后才应用设置 `kubectl rollout pause deployment test-k8s`
* 恢复 `kubectl rollout resume deployment test-k8s`
* 输出到文件 `kubectl get deployment test-k8s -o yaml >> app2.yaml`
* 删除全部资源 `kubectl delete all --all`
---
## Services use label for pod

Service 提供一個不變的 IP 地址和 DNS 名稱，以供其他物件（如 Pods）連接到您的應用程式。

`kubectl apply -f service.yaml` (name should be linked to deployment names)

* Service 通过 label 关联对应的 Pod
* Servcie 生命周期不跟 Pod 绑定，不会因为 Pod 重创改变 IP
* type: 提供了负载均衡功能，自动转发流量到不同 Pod (默认 ClusterIP 集群内可访问，NodePort 节点可访问，LoadBalancer 负载均衡模式（需要负载均衡器才可用）) ->nodeport 要加 port for node
* 可对集群外部提供访问端口
* 集群内部可通过服务名字访问

### svc command
* `kubectl apply -f service.yaml`
* `kubectl get service (svc)`
* `kubectl describe service test-k8s`
---
## StatefulSet
有狀態的應用像是ＤＢ Redis (固定pod的名字) `kubectl apply -f mongo.yaml`  `kubectl get statefulset`
* clusterid is `None`
* Pod 创建和销毁是有序的，创建是顺序的，销毁是逆序的。
* Pod 重建不会改变名字，除了IP，所以不要用IP直连
* 連接pod, `pod-name.service-name`
* pod connect to DB
`kubectl run mongodb-client --rm --tty -i --restart='Never' --image docker.io/bitnami/mongodb:4.4.10-debian-10-r20 --command -- bash`
`mongo --host mongodb-0.mongodb` (connect to pod) `show dbs`

---
## 數據持久化
重啟DB `kubectl rollout restart statefulset mangodb` 資料會不見 可以掛一個storage location, local path, or cloud
1.  (不推薦)persistent volumn,(hostPath 挂载) 只適合用於single node (like minikube) [example link](test_k8s/yaml/deployment/mongo.yaml)
```
# mongo.yaml, kubectl apply -f mongo.yaml
....
      volumes:
        - name: mongo-data              # 卷名字
          hostPath:
            path: /data/mongo-data      # 节点上的路径
            type: DirectoryOrCreate     # 指向一个目录，不存在时自动创建
```

```
in mongodb
> use test
> show dbs
> db.user.save({'_id':'testid', 'name':'hsuan'})
> db.user.find()
{ "_id" : "testid", "name" : "hsuan" }
```
2. `storage class`, `persistence volumne`, `persistence volumne claim`: in cloud service we would only need to create persistence volumne clain, and they would create the PV and storage class for us directly. (we can then connect this storage PVC to the `statefulset`)

however local file we need to define ourselves. 不支持動態創建[example link](test_k8s/yaml/deployment/mongo_pvc.yaml)

---

## confimap & secret

數據庫的path 不應該寫死在檔案裡面應該要用[kind: ConfigMap ](test_k8s/yaml/deployment/configmap.yaml)去設置

```
{url = 'mongodb://mongodb-0.mongodb:27017'
url = `mongodb://${process.env.MONGO_USERNAME}:${process.env.MONGO_PASSWORD}@${process.env.MONGO_ADDRESS}`}
```

還有[kind: Secret](test_k8s/yaml/deployment/secret.yaml)

* `kubectl apply -f configmap.yaml`, `kubectl apply -f secret.yaml`
* `kubectl get configmap mongo-config -o yaml`, `kubectl get secret mongo-secret -o yaml`

---
## namespace (ns)
劃分空間使用 `kubectl get ns`,

* `kubectl get all -n kube-system` : check name space detail,
* `kubectl create namespace {testapp}`  after we create the name space we can then apply the app `kubecl apply -f deployment.yaml --namespace testapp`
* `kubectl get pod --namespace testapp` 查詢時要指定的命名空間才會查詢得到

*可以透過 `kubens` 套件快速切換命名空間*

---
## Ingress: 為外部訪問集群提供統一的入口（避免為外部暴露端口）

需要配合一個cloud service的load balancer + ingress controler, 可以設置不同域名轉發流量到不同service 執行不同pods的工作. Can have domain name and https.

### load balancer example:

```
apiVersion:v1
kind: Service
metadata:
  name: myapp-External-service
spec:
  selector:
    app: myapp
  type: LoadBalancer #open it to public
  ports:
    - protocol: TCP
      port: 8080
      targetPort: 8080
      # external access port
      nodePort: 35010
```
* port: 8080 表示其他 Pods 或 Service 可以在 8080 端口上訪問該 Service。
* targetPort: 8080 表示該 Service 會將流量轉發到選定的 Pods 上的 8080 端口。
* nodePort: 35010 表示你可以直接使用任何節點的 IP 地址，並在 35010 端口上訪問該 Service，然後 Kubernetes 會將該流量轉發到相應的 Service 和 Pod。

### example with ingress (add TLS certificate)

```
# to configure TLS
apiVersion: v1
kind: Secret
metadataL
  name: myapp-secret-tls
  # same namespace as ingress
  namespace: defult
data:
  tls.crt: base64 encoded cert
  tls.key: base64 encoded key
type: kuberbets.io/tls
```

```
apiVersion: networking.k8s.io/v1beta1
kind: Ingress
metadata:
  name: myapp-ingress
spec:
  # https
  tls:
  - hosts:
    - myapp.com
    secretName: myapp-secret-tls
  rules:
  - host: myapp.com
    http:
      path:
      - backend:
          serviceName: myapp-internal-service
          # correspond to the port from the service file
          servicePort: 8080
```

* rules: Router rules: forward request from "myapp.com" to interal service
* host: should be valid domain address and map it to the entrypoint node IP address

```
ex:
apiVersion:v1
kind: Service
metadata:
  name: myapp-internal-service
spec:
  selector:
    app: myapp
  ports:
    - protocol: TCP
      port: 8080
      targetPort: 8080
```

* no nodePort
* instead of Loadbalancer type we use defult type ClusterIp

### before setting up

we need to install **Ingress Controller** pod, one of them is **K8s Nginx Ingress Controller**. if we are using cloud service, the external requests would first hit the **Cloud Load Balancer** then it would redirect the traffic to ingress controller. (load balancer would be auto implemented on the cloud.)

### ingress on Minikube

* install ingress controller in minikube `minikube addons enable ingress`
* `kubectl get pod -n kube-system`: we can see nginx
