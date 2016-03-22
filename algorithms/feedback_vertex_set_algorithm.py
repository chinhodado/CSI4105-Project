from abc import ABCMeta, abstractmethod


class FeedbackVertexSetAlgorithm(object):
    """
    An abstract class for an algorithm that solves the feedback vertex set problem
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_fbvs(self, graph) -> set:
        """
        Get a feedback vertex set of the given graph. May or may not be optimal.
        This will return a set of vertex whose removal will make the graph acyclic.
        This is mainly for optimization form problems.
        :param graph: The graph to solve
        :return: A feedback vertex set for the graph
        """
        pass

    @abstractmethod
    def get_fbvs_max_size(self, graph, k) -> set:
        """
        Get a feedback vertex set of size at most k. Return None if no such fbvs exists.
        This is mainly for decision form problems.
        :param graph: The graph to solve
        :param k: The maximum size for the fbvs
        :return: A fbvs of size at most k, or None if no such fbvs exists
        """
        pass
