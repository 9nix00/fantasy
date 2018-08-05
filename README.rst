Fantasy
========

|build-status| |coverage|


Flask 应用框架。



Fantasy 设计思路
--------------------
`Flask`_ 是一款 **microframework** 风格的框架，

基于Flask构造的App也理应保持该风格，所以在Flask中加入太多的功能是不必要的。


我们调研过一些Flask的上层框架，就个人而言，我并不是特别认同这些项目的实现，在我看来不少Flask上层实现属于过度设计。

Flask应该保持其简单灵活的特性。如果封装过度，我为什么不使用更完整更成熟的 `Django`_ 呢？


我们不能因为喜爱Flask，而把一些成熟的开源框架，比如Django的优点移植过来，有时候这些优点对Flask没好处。

Flask最大的价值在于，基于 **microframework** 的设计使得我们在构建微服务架构时，在App层开发效率得以极大的提升。

但是回到现实，如果完全不依赖更高级的封装，在使用Flask时，又会增加了比较多的工作量。

`Fantasy`_ 的目标就在此，在保持Flask简洁的同时，提供一层通用的组件，提升开发效率。

我们的目标很清晰，我们不是为了移植已经成熟框架的功能，而是应该聚焦于新的架构：**微服务**


    如何在微服务架构中，更快速的开发，实现更轻量的应用集，才应该是Flask关注的。


当然，理想很丰满，现实很骨感。

在保持小巧和开发高效之间，这个平衡点并没有描述的这么轻松。

目前我们还在尝试中，所以这还是一个不稳定的项目，虽然在我们的项目中，已经开始正式使用。
**在生产环境你应该慎重使用**。


.. _Fantasy: https://github.com/wangwenpei/fantasy
.. _Flask: http://flask.pocoo.org/
.. _Django: https://www.djangoproject.com/



.. |build-status| image:: https://secure.travis-ci.org/wangwenpei/fantasy.png?branch=master
    :alt: Build status
    :target: https://travis-ci.org/wangwenpei/fantasy

.. |coverage| image:: https://codecov.io/github/wangwenpei/fantasy/coverage.svg?branch=master
    :target: https://codecov.io/github/wangwenpei/fantasy?branch=master

