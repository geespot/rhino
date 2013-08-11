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
    2. git checkout -b %featurebranch%
    3. git push origin %featurebranch% (将你的开发推送到你的fork)
    4. 进行开发
    5. git add xxxx
    6. git commit
    7. 重复 4 - 6
    8. 完成以后，git push，建议在4-6的时候也时不时的push一下，这样别人可以看到你的代码进度

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

