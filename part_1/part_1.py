"""
NB:
    - can take multiple author names
    - support empty spaces between tags or author names separated by commas
    - intents to avoid duplicates
    - commands and values are case-insensitive
    - commands rtag, rname support shortcuts of the values (e.g. 'li' for 'life'/'live')
"""
import redis
import sys

from redis_lru import RedisLRU
from typing import List, Any

from models import Author, Quote
from myexception import MyException
from utils import print_result_author, print_result_tag

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


@cache
def find_by_tag_regex(tag: str) -> list[str | None]:
    #print(f"Find by {tag}")
    quotes = Quote.objects(tags__iregex=tag)
    result = {q.quote for q in quotes}
    return result


@cache
def find_by_tag(tag: str) -> list[str | None]:
    #print(f"Find by '{tag}'")
    quotes = Quote.objects(tags__iexact=tag)
    result = {q.quote for q in quotes}
    return result


@cache
def find_by_author_regex(author: str) -> list[list[Any]]:
    #print(f"Find by '{author}'")
    authors = Author.objects(fullname__iregex=author)
    result = {}
    for a in authors:
        quotes = Quote.objects(author=a)
        result[a.fullname] = {q.quote for q in quotes}
    return result


@cache
def find_by_author(author: str) -> list[list[Any]]:
    #print(f"Find by '{author}'")
    authors = Author.objects(fullname__iexact=author)
    result = {}
    for a in authors:
        quotes = Quote.objects(author=a)
        result[a.fullname] = {q.quote for q in quotes}
    return result


def tag_handler(args):
    res = set()
    #print(args)
    for tag in args:
        res.update(find_by_tag(tag))
    return print_result_tag(res)


def rtag_handler(args):
    res = set()
    #print(args)
    for tag in args:
        res.update(find_by_tag_regex(tag))
    return print_result_tag(res)


def author_handler(args):
    res = []
    for author in args:
        res.append(find_by_author(author))
    return print_result_author(res)


def rauthor_handler(args):
    res = []
    for author in args:
        res.append(find_by_author_regex(author))
    return print_result_author(res)


def exit_handler(*args):
    print("Exiting the programme. See you next time, bye! ;-D")
    sys.exit(0)


COMMAND2HANDLER = {
    "name": author_handler,
    "tag": tag_handler,
    "rname": rauthor_handler,
    "rtag": rtag_handler,
    "exit": exit_handler
}


def command_handler(user_input: str):
    if not user_input or not isinstance(user_input, str):
        raise MyException("Please, enter your command.")
    command, *args = user_input.split(":")
    command = command.lower()
    if command not in COMMAND2HANDLER:
        raise MyException(f"The command '{command}' is not known. Possible commands are: {list(COMMAND2HANDLER.keys())}. "
                          f"Please, try again. ")
    tgt_handler = COMMAND2HANDLER[command]
    if args:
        args = args[0].split(",")
        args = {el.strip() for el in args}
    #print("args: ", args)
    return tgt_handler, args


def main():
    while True:
        user_input = input("Please, enter your command (auther: value(s) | tag: value(s) | exit): ")
        try:
            handler, args = command_handler(user_input)
            result = handler(args)
            print(result)
        except MyException as e:
            print(e)


if __name__ == '__main__':
    main()
    """
    print(find_by_tag('mi'))
    print(find_by_tag('mi'))

    print(find_by_author('in'))
    print(find_by_author('in'))
    quotes = Quote.objects().all()
    print([e.to_json() for e in quotes])
    """
