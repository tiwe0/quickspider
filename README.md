# QuickSpider

Thid is a samll spider framework which based on nodes and graph built with these nodes.

The goal of this samll framework is to build a quick spider.

## 安装

使用 pip

```bash
pip install quickspider
```

## 如何使用？

1. 自定义你的节点。（或使用其他人写的节点、内置节点）
2. 使用节点构建爬取图。（配置 toml 文件）
3. 运行。

## TODO

- [ ] 动态扫描节点类
- [ ] 添加节点间的组合
- [*] 解析器(50%)
- [ ] add more parse method like xpath, regex...
- [ ] 添加日志系统
- [ ] 尝试添加并发
- [ ] 提高鲁棒性
- [ ] 添加更多内置节点
- [ ] 分享节点的站点
- [ ] gui编辑器
- [ ] more and more...

## 当前版本的样例

1. 使用默认模板创建图。

```bash
quickspiderrun create --template default
```

2. 直接运行默认图。

```bash
quickspiderrun run --file deafult.toml
```

## 说明

### 谁需要它？

`quickspider`是一个类似玩具的小框架，如果你需要大量，并发，稳定的爬取，那么请使用`scrapy`；如果你需要对付一些刁钻的小网站，那么请使用`requests`、`httpx`、`beautifulsoup`等库自定义你的爬虫。

那么，`quickspider`存在的意义是什么呢？`quickspider`旨在协同你完成两件事：

1. 快速的开发一个常规的，数据量不是那么大的小爬虫；

2. 验证你在开发大型或更灵活的爬虫时的idea。

所以请不要将其作为专业的爬虫工具。

### 这个东西是怎么实现的？

`quickspider`的想法非常简单，quickspider中包含各种各样的节点，这些节点可能是你自己编写的（请参考编写手册），也可能是别人编写的（请参考这个人写的帮助文档），也可能是内置的（请参考内置节点说明）。使用toml文档声明，配置这些节点，并将这些节点构造成一棵树，之后即可使用这个树指导quickspider进行爬取。

爬取的本质是数据信息的变换，而具体执行变换的，就是节点。由节点构成的树便形成了一个数据变换流。

### 这个toml究竟在说啥？

```toml
[nodes] 

[nodes.url]
type = "PageNode"
input = "http://quotes.toscrape.com/page/{page}/"
start = 1
stop = 6

[nodes.Geter]
type = "GetNode"
```

[nodes]声明了节点集合。

[nodes.NodeName]声明了具体的节点，NodeName无关紧要，仅用于方便开发者；前缀`nodes.`不可省略。

[nodes.NodeName]下面的`key = value`则指明了该节点的属性。

其中`type`为每个节点必不可少的属性，该属性声明了该节点的种类；余下的属性则根据节点种类的不同而有所区别。

1. 比如[nodes.url]:

该节点的名称为`url`，类别为`PageNode`。这是个内置的节点类别，该节点的作用为将`input`以`page`为关键字，以[start, stop)作为区间，作一个格式化处理。其中还有一个参数为step，默认为1，因此可以省去。

2. 比如[nodes.Geter]:

该节点的名称为`Geter`，类别为`GetNode`。这也是个内置的节点类别。该节点会将URL转换为Response。


