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
1.  (不推薦)persistent volumn,(hostPath 挂载) 只適合用於single node (like minikube)
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
2. storage class, persistence volumne, persistence volumne claim
