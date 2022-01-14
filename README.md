# QuickSpider

Thid is a samll spider framework which based on nodes and graph built with these nodes.

The goal of this samll framework is to build a quick spider.

## How to use it？

1. custome your nodes. (or use nodes writen by others or builtin nodes)
2. build graph using the nodes. (use toml file)
3. run it.

## TODO

- [ ] add node operation like node combination
- [ ] parser to define the nodes and construct the graph. (maybe use syntax like markdown)
- [ ] add more parse method like xpath, regex...
- [ ] add logger system
- [ ] try to add asyn feature
- [ ] robust
- [ ] some useful nodes for spider builders
- [ ] maybe a market place to share your nodes.
- [ ] add gui editor
- [ ] more and more...

## Example for current version

```bash
quickspider create --template default
```

then, you can find one toml file: default.toml

```bash
quickspider run --file deafult.toml
```

