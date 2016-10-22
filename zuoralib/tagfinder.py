import bs4


class TagNotFound(Exception):
    pass


class TagFinder(object):

    """
        Utility class using Beautiful Soup, but adding some more
        checks in order to raise exceptions when the expetected
        conditions are not met.
    """

    @staticmethod
    def find_at_least_one(tag, *args, **kwargs):
        """
            :param tag: the tag element to search in
            :param args: same as BeautifulSoup.find_all
            :param kwargs: same as BeautifulSoup.find_all
            :return: a list of at least one tag element
            If not found, raises a TagNotFound Exception
        """
        found = tag.find_all(*args, **kwargs)
        if len(found) < 1:
            raise TagNotFound('could not find: %s, %s' % (args, kwargs))
        return found

    @staticmethod
    def find_exactly(tag, count, *args, **kwargs):
        """
            :param tag: the tag element to search in
            :param count: the number of expected matches
            :param args: same as BeautifulSoup.find_all
            :param kwargs: same as BeautifulSoup.find_all
            :return: a list of at least one tag element
            If not found, raises a TagNotFound Exception
        """
        found = tag.find_all(*args, **kwargs)
        if len(found) != count:
            raise TagNotFound('could not find %d occurences, found %d' % (count, len(found)))
        return found

    @staticmethod
    def find_tag(tag, *args, **kwargs):
        """
            :param tag: the tag element to search in
            :param args: same as BeautifulSoup.find
            :param kwargs: same as BeautifulSoup.find
            :return: first tag element found
            If not found, raises a TagNotFound Exception
            """
        found = tag.find(*args, **kwargs)
        if not found:
            raise TagNotFound('could not find: %s, %s' % (args, kwargs))
        return found

    @staticmethod
    def find_tag_by_contents(tag, contents, *args, **kwargs):
        """
            :param tag: the tag element to search in
            :param args: same as BeautifulSoup.find
            :param kwargs: same as BeautifulSoup.find
            :return: first tag element found
            If not found, raises a TagNotFound Exception
            """
        found = tag.find_all(*args, **kwargs)
        if not len(found):
            raise TagNotFound('could not find: %s, %s' % (args, kwargs))
        for f in found:
            if hasattr(f, 'contents'):
                if f.contents[0].strip() == contents:
                    return f
        raise TagNotFound('could not find: %s, %s with contents %s' % (args, kwargs, contents))

    @staticmethod
    def find_first_sibling_tag(tag):
        """
            :param tag: a bs4.element.Tag instance
            :return: the first sibling which is a tag
            If there is no sibling, raises TagNotFound
        """
        sibling = tag.next_sibling
        while sibling is not None and type(sibling) != bs4.element.Tag:
            sibling = sibling.next_sibling
        if not sibling:
            raise TagNotFound('could not find a sibling tag to %s' % tag.name)
        return sibling
