# Docker 容器化平台

## 核心概念
- **镜像(Image)**：只读模板，包含运行应用所需的一切
- **容器(Container)**：镜像的运行实例，包含应用和运行环境
- **仓库(Repository)**：存储镜像的地方，Docker Hub是最大的公共仓库
- **Dockerfile**：构建镜像的脚本文件，包含构建指令

## 镜像操作
```bash
# 拉取镜像
docker pull nginx                   # 拉取最新版本
docker pull nginx:1.20              # 拉取指定版本
docker pull ubuntu:20.04            # 拉取Ubuntu 20.04

# 查看本地镜像
docker images                       # 查看所有镜像
docker image ls                     # 同上
docker images --filter "dangling=true" # 查看悬空镜像
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" # 格式化输出

# 删除镜像
docker rmi nginx                    # 删除镜像
docker rmi $(docker images -q)      # 删除所有镜像
docker image prune                  # 删除未使用的镜像
docker image prune -a               # 删除所有未使用的镜像

# 构建镜像
docker build -t my-app .            # 构建镜像
docker build -t my-app:v1.0 .      # 构建带标签的镜像
docker build -f Dockerfile.prod .   # 使用指定的Dockerfile
docker build --no-cache -t my-app . # 不使用缓存构建

# 镜像标签
docker tag my-app:latest my-app:v1.0 # 给镜像打标签
docker tag my-app:latest registry.com/my-app:latest # 标记为私有仓库
```

## 容器操作
```bash
# 运行容器
docker run nginx                    # 运行容器
docker run -d nginx                 # 后台运行
docker run -p 8080:80 nginx         # 端口映射
docker run -p 8080:80 -p 443:443 nginx # 多个端口映射
docker run -v /host/path:/container/path nginx # 挂载卷
docker run -e NODE_ENV=production nginx # 环境变量
docker run --name my-nginx nginx    # 指定容器名称
docker run --rm nginx               # 容器停止后自动删除

# 查看容器
docker ps                           # 查看运行中的容器
docker ps -a                        # 查看所有容器
docker ps --filter "status=exited"  # 查看已停止的容器
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" # 格式化输出

# 容器管理
docker start <container>            # 启动容器
docker stop <container>             # 停止容器
docker restart <container>          # 重启容器
docker pause <container>            # 暂停容器
docker unpause <container>          # 恢复容器
docker kill <container>             # 强制停止容器

# 删除容器
docker rm <container>               # 删除容器
docker rm -f <container>            # 强制删除运行中的容器
docker rm $(docker ps -aq)          # 删除所有容器
docker container prune              # 删除停止的容器
```

## 容器交互
```bash
# 进入容器
docker exec -it <container> bash    # 进入容器bash
docker exec -it <container> sh      # 进入容器sh
docker exec -it <container> /bin/bash # 指定shell

# 查看容器信息
docker logs <container>             # 查看容器日志
docker logs -f <container>          # 实时查看日志
docker logs --tail 100 <container>  # 查看最后100行日志
docker logs --since 2h <container>  # 查看2小时内的日志

docker inspect <container>          # 查看容器详细信息
docker stats <container>            # 查看容器资源使用
docker top <container>              # 查看容器进程
docker port <container>             # 查看端口映射

# 文件操作
docker cp file.txt <container>:/path/ # 复制文件到容器
docker cp <container>:/path/file.txt ./ # 从容器复制文件
```

## Dockerfile 语法
```dockerfile
# 基础镜像
FROM node:16-alpine               # 使用Alpine Linux版本(更小)
FROM ubuntu:20.04                 # 使用Ubuntu 20.04
FROM python:3.9-slim              # 使用Python 3.9精简版

# 设置工作目录
WORKDIR /app                      # 设置工作目录

# 复制文件
COPY package*.json ./             # 复制package文件
COPY src/ ./src/                  # 复制源代码目录
ADD https://example.com/file.tar.gz /tmp/ # 复制URL文件(支持解压)

# 执行命令
RUN apt-get update && apt-get install -y curl # 安装软件包
RUN npm install                   # 安装依赖
RUN pip install -r requirements.txt # 安装Python依赖

# 环境变量
ENV NODE_ENV=production           # 设置环境变量
ENV API_URL=https://api.example.com
ENV PORT=3000

# 暴露端口
EXPOSE 3000                       # 暴露端口
EXPOSE 80 443                     # 暴露多个端口

# 启动命令
CMD ["npm", "start"]              # 默认启动命令
CMD ["python", "app.py"]          # Python应用启动
ENTRYPOINT ["python", "app.py"]   # 入口点(不能被覆盖)

# 用户设置
USER node                         # 切换到node用户
USER 1001                         # 切换到指定UID用户

# 卷挂载
VOLUME ["/data"]                  # 声明挂载点
```

## 多阶段构建
```dockerfile
# 构建阶段
FROM node:16 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# 生产阶段
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## Docker Compose
```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgresql://user:pass@db:5432/myapp
    depends_on:
      - db
      - redis
    volumes:
      - ./logs:/app/logs
    networks:
      - app-network

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=myapp
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - app-network

  redis:
    image: redis:6-alpine
    ports:
      - "6379:6379"
    networks:
      - app-network

volumes:
  postgres_data:

networks:
  app-network:
    driver: bridge
```

```bash
# Docker Compose命令
docker-compose up                 # 启动所有服务
docker-compose up -d              # 后台启动
docker-compose up --build         # 构建并启动
docker-compose up web             # 只启动web服务

docker-compose down               # 停止所有服务
docker-compose down -v            # 停止并删除卷
docker-compose down --rmi all     # 停止并删除镜像

docker-compose build              # 构建所有服务
docker-compose build web          # 构建指定服务
docker-compose build --no-cache   # 不使用缓存构建

docker-compose ps                 # 查看服务状态
docker-compose logs               # 查看所有服务日志
docker-compose logs web           # 查看指定服务日志
docker-compose logs -f web        # 实时查看日志

docker-compose exec web bash      # 进入web服务容器
docker-compose exec db psql -U user -d myapp # 进入数据库
```

## 网络管理
```bash
# 网络操作
docker network ls                 # 查看网络列表
docker network create my-network  # 创建网络
docker network inspect my-network # 查看网络详情
docker network rm my-network      # 删除网络

# 容器网络
docker run --network my-network nginx # 使用指定网络
docker run --network host nginx       # 使用主机网络
docker run --network none nginx       # 不使用网络

# 网络类型
# bridge: 默认网络，容器间可以通信
# host: 使用主机网络栈
# none: 禁用网络
# overlay: 跨主机网络(Swarm模式)
```

## 卷管理
```bash
# 卷操作
docker volume ls                  # 查看卷列表
docker volume create my-volume    # 创建卷
docker volume inspect my-volume   # 查看卷详情
docker volume rm my-volume        # 删除卷
docker volume prune               # 删除未使用的卷

# 使用卷
docker run -v my-volume:/data nginx # 使用命名卷
docker run -v /host/path:/container/path nginx # 绑定挂载
docker run -v /host/path:/container/path:ro nginx # 只读挂载

# 卷备份
docker run --rm -v my-volume:/data -v $(pwd):/backup ubuntu tar czf /backup/data.tar.gz /data
docker run --rm -v my-volume:/data -v $(pwd):/backup ubuntu tar xzf /backup/data.tar.gz -C /data
```

## 资源限制
```bash
# 内存限制
docker run -m 512m nginx          # 限制内存为512MB
docker run -m 1g nginx            # 限制内存为1GB
docker run --memory-swap 1g nginx # 限制内存+交换空间

# CPU限制
docker run --cpus="1.5" nginx     # 限制CPU为1.5核
docker run --cpuset-cpus="0,1" nginx # 限制使用CPU 0和1

# 其他限制
docker run --pids-limit 100 nginx # 限制进程数
docker run --ulimit nofile=1024:1024 nginx # 限制文件描述符
```

## 常用镜像
```bash
# Web服务器
docker run -d -p 80:80 nginx      # Nginx
docker run -d -p 8080:80 httpd    # Apache

# 数据库
docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=password postgres:13
docker run -d -p 3306:3306 -e MYSQL_ROOT_PASSWORD=password mysql:8.0
docker run -d -p 6379:6379 redis:6-alpine
docker run -d -p 27017:27017 mongo:4.4

# 开发环境
docker run -it node:16 bash       # Node.js环境
docker run -it python:3.9 bash   # Python环境
docker run -it ubuntu:20.04 bash  # Ubuntu环境
docker run -it alpine:latest sh   # Alpine环境

# 工具
docker run -it --rm alpine/git    # Git工具
docker run -it --rm curlimages/curl # curl工具
docker run -it --rm nicolaka/netshoot # 网络调试工具
```

## 清理和维护
```bash
# 清理命令
docker system prune               # 清理未使用的资源
docker system prune -a            # 清理所有未使用的资源
docker system prune -f            # 强制清理，不询问

# 分别清理
docker container prune            # 清理停止的容器
docker image prune                # 清理未使用的镜像
docker volume prune               # 清理未使用的卷
docker network prune              # 清理未使用的网络

# 查看磁盘使用
docker system df                  # 查看Docker磁盘使用情况
docker system df -v               # 详细显示
```

## 镜像导出导入
```bash
# 导出镜像
docker save nginx > nginx.tar     # 导出镜像到文件
docker save nginx:1.20 > nginx.tar # 导出指定版本
docker save -o nginx.tar nginx    # 使用-o参数

# 导入镜像
docker load < nginx.tar           # 从文件导入镜像
docker load -i nginx.tar          # 使用-i参数

# 导出容器
docker export <container> > container.tar # 导出容器为tar文件
docker import container.tar my-image:latest # 从tar文件创建镜像
```

## 故障排查
```bash
# 查看容器日志
docker logs <container>           # 查看容器日志
docker logs --details <container> # 查看详细日志

# 进入容器调试
docker exec -it <container> bash # 进入容器
docker exec -it <container> sh   # 进入容器(Alpine)

# 检查容器状态
docker inspect <container>       # 查看容器详细信息
docker stats <container>         # 查看资源使用情况
docker top <container>           # 查看容器进程

# 网络问题
docker network ls                # 查看网络
docker network inspect bridge    # 检查默认网络
ping <container-ip>             # 测试网络连通性

# 重启Docker服务
sudo systemctl restart docker    # Linux
sudo service docker restart      # Linux(旧版本)
```

## 安全最佳实践
```dockerfile
# 使用非root用户
FROM node:16-alpine
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001
USER nextjs

# 最小化镜像
FROM node:16-alpine AS builder
# 构建阶段...

FROM node:16-alpine
RUN addgroup -g 1001 -S nodejs && adduser -S nextjs -u 1001
COPY --from=builder --chown=nextjs:nodejs /app /app
USER nextjs
```

## 性能优化
```bash
# 构建优化
docker build --target production . # 多阶段构建指定阶段
docker build --build-arg BUILDKIT_INLINE_CACHE=1 . # 启用内联缓存

# 运行优化
docker run --memory=512m --cpus=1.0 nginx # 资源限制
docker run --shm-size=1g nginx      # 共享内存大小
docker run --tmpfs /tmp:rw,size=100m nginx # 临时文件系统
```