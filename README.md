# Fantasy

![](https://secure.travis-ci.org/wangwenpei/fantasy.png?branch=master)
![](https://codecov.io/github/wangwenpei/fantasy/coverage.svg?branch=master)


[Flask](http://flask.pocoo.org/) 应用层框架。


Fantasy 设计思路
--------------------
[Flask](http://flask.pocoo.org/) 是一款 **microframework** 风格的框架，

基于Flask构造的App也理应保持该风格，所以在Flask中加入太多的功能是不必要的。


我们调研、使用过一些Flask的上层框架，就个人而言，我并不是特别认同这些项目的实现，在我看来不少Flask上层实现属于过度设计。

[Flask](http://flask.pocoo.org/) 应该保持其简单灵活的特性。如果封装过度，我为什么不使用更完整更成熟的 [Django](https://www.djangoproject.com/)


[Flask](http://flask.pocoo.org/) 最大的价值在于，基于 **microframework** 的设计使得我们在构建微服务架构时，在App层开发效率得以极大的提升。

但是回到现实，如果完全不依赖更高级的封装，在使用[Flask](http://flask.pocoo.org/) 时，又会增加了比较多的工作量。

[Fantasy](https://github.com/wangwenpei/fantasy)的目标就在此，在保持Flask简洁的同时，提供一层通用的组件，提升开发效率。

我们的目标很清晰，我们不是为了移植已经成熟框架的功能，而是应该聚焦于新的架构：**微服务**


    如何在微服务架构中，更快速的开发，实现更轻量的应用集，才应该是Flask关注的。


当然，理想很丰满，现实很骨感。

在保持小巧和开发高效之间，这个平衡点并没有描述的这么轻松。

目前我们还在尝试中，所以这还是一个不稳定的项目，虽然在我们的项目中，已经开始正式使用。
**在生产环境你应该慎重使用**。
