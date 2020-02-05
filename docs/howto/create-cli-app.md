# 创建CLI APP



## 构造过程

### 规划CLI APP

构造`cli.py`,基于flask 所使用的 `click` 框架实现。

```
import click


@click.group()
def generic():
    """
    入口
    """
    pass


@generic.command()
@click.option('--hello')
def hello(hello):
    click.echo('hello')
    pass

```


### 与 Fantasy 绑定

在 `__init__.py` 构造 `run_cli(app)`

e.g

```

from .cli import generic

def run_cli(app):
    app.cli.add_command(generic)
    pass

```

### 撰写测试用例


#### 配置默认入口

`tests/conftest.py`

```

import pytest
from click.testing import CliRunner

pytest_plugins = "app_fixtures.myapp",  # 固定声明，引入扩展


def pytest_namespace():
    return {
        'entry_app': 'raw_transaction',  # 指定入口，通常是包名
        'cli_runner': CliRunner(),
    }


@pytest.fixture(scope='function')
def cli_runner():
    """custom cli runner,
    if you really need it.
    """
    return CliRunner()


```

#### 撰写测试用例

`tests/test_*.py`

```





```


















