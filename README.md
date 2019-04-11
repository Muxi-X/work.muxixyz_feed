# work.muxixyz_feed

部署：

1,using `nohup python3 manage.py receive` to deploy feed receive process <br>
2,using `sh start.sh &` to deploy api process <br>


# MQ k8s 部署

不使用docker&k8s部署见: https://cgh233.github.io/2019/03/29/RabbitMQ%E5%85%A5%E9%97%A8/ 


deploy.yaml

```yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: rabbitmq
  namespace: workbench
  labels:
    run: rabbitmq1
spec:
  replicas: 1
  template:
    metadata:
      labels:
        run: rabbitmq1
    spec:
      containers:
      - name: rabbitmq1
        image: rabbitmq:3-management
        args:
          - rabbitmq-server
        env:
          - name: RABBITMQ_DEFAULT_USER
            value: "username"
          - name: RABBITMQ_DEFAULT_PASS
            value: "password"
        ports:
          - containerPort: 5672
```

svc.yaml 

```
apiVersion: v1
kind: Service
metadata:
  namespace: workbench
  labels:
    run: rabbitmq1
  name: rabbitmq1
spec:
  ports:
  - port: 5672
    targetPort: 5672
    protocol: TCP
  selector:
    run: rabbitmq1
```

