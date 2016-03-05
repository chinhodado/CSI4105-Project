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
        :param graph: The graph to solve
        :return: A feedback vertex set for the graph
        """
        pass
