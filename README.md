[![PyPI](https://img.shields.io/pypi/v/perplexityai)](https://pypi.org/project/perplexityai)
[![Downloads](https://static.pepy.tech/badge/perplexityai)](https://pypi.org/project/perplexityai)
[![Status](https://img.shields.io/pypi/status/perplexityai)](https://pypi.org/project/perplexityai)

# perplexityai

A simple module to use Perplexity AI in Python.

## Get started:

```
python -m pip install -U perplexityai
```

Join my [Discord server](https://dsc.gg/devhub-rsgh) for live chat, support, or if you have any issues with this package.

## Support this repository:
- ⭐ **Star the project:** Star this repository. It means a lot to me! 💕
- 🎉 **Join my Discord Server:** Chat with me and others. [Join here](https://dsc.gg/devhub-rsgh):

[![DiscordWidget](https://discordapp.com/api/guilds/1137347499414278204/widget.png?style=banner2)](https://dsc.gg/devhub-rsgh)

## Example:

```python
from perplexityai import Perplexity

prompt = input("👦: ")
for a in Perplexity().generate_answer(prompt):
    print(f"🤖: {a['answer']}")
```

*Thanks to [nathanrchn/perplexityai]("https://github.com/nathanrchn/perplexityai") for the original code.*