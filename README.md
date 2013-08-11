rhino
=====

获取代码以及配置环境

    1. 注册账号, 登陆
    2. https://github.com/yibaisoft/rhino ==> 点击Fork
    3. 下载GIT客户端以及命令行工具
    4. 在GIT命令行下进入你的工作目录
    5. git clone https://github.com/%username%/rhino.git (将你的fork克隆到本地）
    6. cd rhino
    7. git remote add upstream git://github.com/yibaisoft/rhino （将团队工程设置为upstream）

=====

同步服务器代码

    1. git checkout master  （切换到master）
    2. git fetch upstream   （获取团队的master代码）
    3. git merge upstream/master （更新本地master）


======

进行开发

    1. 同步服务器代码
    2. git checkout -b featurebranch
    3. 进行开发
    4. git add xxxx
    5. git commit
    6. 重复 3 - 5
    7. 完成以后，git push (将你的开发推送到你的fork）

=====

提交代码

    1. 登陆github
    2. 进入http://github.com/%username%/rhino
    3. 找到你要提交的branch
    4. 点击pull request，往yibaisoft/master，发送提交
    5. 找其他的同学进行code review

=====

审核代码

    1. 登陆github
    2. 进入http://github.com/yibaisoft/rhino
    3. 进入pull requests, 找到需要review的branch
    4. 如果通过，则merge branch，否则，close掉

