[![PyPI](https://img.shields.io/pypi/v/perplexityai)](https://pypi.org/project/perplexityai)
[![Downloads](https://static.pepy.tech/badge/perplexityai)](https://pypi.org/project/perplexityai)
[![Status](https://img.shields.io/pypi/status/perplexityai)](https://pypi.org/project/perplexityai)

# perplexityai

A better, simpler, and faster version of nathanrchn's PerplexityAI.

## Get started:

```
python -m pip install -U perplexityai
```

Join my [Discord server](https://discord.com/invite/UxJZMUqbsb) for live chat, support, or if you have any issues with this package.

## Support this repository:
- ⭐ **Star the project:** Star this repository. It means a lot to me! 💕
- 🎉 **Join my Discord Server:** Chat with me and others. [Join here](https://discord.com/invite/UxJZMUqbsb):

[![DiscordWidget](https://discordapp.com/api/guilds/1137347499414278204/widget.png?style=banner2)](https://discord.com/invite/UxJZMUqbsb)

## Example:

```python
import perplexityai
from asyncio import run


async def main():
    while True:
        prompt = input("👦: ")
        try:
            resp = await perplexityai.Completion().create(prompt)
            print(f"🤖: {resp}")
        except Exception as e:
            print(f"🤖: {e}")


run(main())
```
