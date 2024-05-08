[![PyPI](https://img.shields.io/pypi/v/perplexityai)](https://pypi.org/project/perplexityai)
[![Downloads](https://static.pepy.tech/badge/perplexityai)](https://pypi.org/project/perplexityai)
[![Status](https://img.shields.io/pypi/status/perplexityai)](https://pypi.org/project/perplexityai)

# perplexityai

A simple module to use Perplexity AI in Python.

## Get started:

```
python -m pip install -U perplexityai
```

## Support this repository:
- ⭐ **Star the project:** Star this repository. It means a lot to me! 💕

## Example:

### Perplexity:
```python
from perplexityai import Perplexity

prompt = input("👦: ")
for a in Perplexity().generate_answer(prompt):
    print(f"🤖: {a['answer']}")
```

### Labs:
```python
"""
Models:
[
    "mixtral-8x7b-instruct",
    "llava-7b-chat",
    "llama-2-70b-chat",
    "codellama-34b-instruct",
    "mistral-7b-instruct",
    "pplx-7b-chat",
    "pplx-70b-chat",
    "pplx-7b-online",
    "pplx-70b-online",
]
"""
from perplexityai import Labs

prompt = input("👦: ")
for r in Labs().generate_answer(prompt, "MODEL"): 
    print(f"🤖: {r['output']}")
```

*Thanks to [nathanrchn's perplexityai](https://github.com/nathanrchn/perplexityai) for the original code.*
