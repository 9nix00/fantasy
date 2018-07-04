Fantasy
========

Flask 轻量级应用框架。

Fantasy 设计思路
--------------------
`Flask`_ 是一款 microframework 风格的框架。
基于Flask构造的App也理应保持该风格。所以在Flask中加入太多的功能是不必要的。

我看过一些Flask的上层框架，就个人而言，我并不喜欢这些项目的实现，在我看来属于过度设计。
Flask应该保持其简单灵活的特性。如果封装过度，我为什么不使用更完整更成熟的 `Django`_ 呢？

我们不能为了喜爱Flask，而去盲目的改造Flask。
Flask最大的价值在于，基于microframework的设计使得我们在构建微服务架构时，在App层开发效率得以极大的提升。
而如果完全不依赖更高级的封装，在使用Flask时，又增加了比较多的工作量。

`Fantasy`_ 的目标就在此，在保持Flask简洁的同时，提供一层通用的组件，提升开发效率。

.. _Fantasy: https://github.com/wangwenpei/fantasy
.. _Flask: http://flask.pocoo.org/
.. _Django: https://www.djangoproject.com/
