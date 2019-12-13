# work.muxixyz_feed

部署：

1,using `nohup python3 manage.py receive` to deploy feed receive process <br>
2,using `sh start.sh &` to deploy api process <br>

# Feed Structure

```json 
{
        "user": {   
            "name": "string",
            "id": "integer",
            "avatar_url": "string"
        },
        "action": "string",
        "feedid": "integer", // feed本身的id
        "ifsplit": "boolean", // 是否有分割线
        "source": {
            "kind_id": "integer",    // kind_id
            "object_id": "integer",  // object id
            "object_name": "string", // object名字
            "project_id": "integer", // 没有为-1,如进度就没有projectid
            "project_name": "string" // project名字，没有为 "noname"
        },
        "timeday": "2019/12/13",  // 2019年12月13日
        "timehm": "00:54"         // 00点54分
}
user object: 用户信息，包括用户名，用户id以及头像
action: 用户执行的动作，直接给出的就是可以使用的动作名，包括 "加入", "创建", "编辑", "删除", "评论", "移动" 。
source: feed的来源. 其中kind_id的对应关系如下
1 -> 团队
2 -> 项目
3 -> 文档
4 -> 文件
5 -> ???
6 -> 进度  // 估计是当时写进度的那个人数错了 把6当成进度了，5没有内容  = =

```

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

