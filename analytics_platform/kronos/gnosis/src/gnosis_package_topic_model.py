from analytics_platform.kronos.gnosis.src.abstract_gnosis import AbstractGnosis
from analytics_platform.kronos.gnosis.src.gnosis_constants import *


class GnosisPackageTopicModel(AbstractGnosis):
    """Package Topic Model that learns topics associated with a package."""

    def __init__(self, dictionary):
        """Instantiate Package Topic Model."""

        self._dictionary = dictionary

    @classmethod
    def train(cls, data_store):
        """:param data_store: The source for input data files.
        :return: package_topic model."""

        # TODO: Train a package topic model from the data available in the given
        # data source. The input data is a collection of GitHub details like
        # package description, etc.

        raise NotImplementedError
        return None

    @classmethod
    def curate(cls, data_store, filename):
        """Reads curated package topic dict from the given store and makes every element
        to lower case, regenerates the package topic map and generated the topic to package map.

        :param data_store: Data store to read curated package to topic data from
        :param filename: name of the file containing curated data

        :return: Object of class GnosisPackageTopicModel."""

        eco_to_package_topic_json_array = data_store.read_json_file(filename)
        eco_to_package_topic_dict = dict()
        eco_to_package_to_topic_dict = dict()
        eco_to_topic_to_package_dict = dict()

        for eco_to_package_topic_json in eco_to_package_topic_json_array:
            ecosystem = eco_to_package_topic_json.get(GNOSIS_PTM_ECOSYSTEM)
            package_topic_dict = dict(
                eco_to_package_topic_json.get(GNOSIS_PTM_PACKAGE_TOPIC_MAP))
            package_to_topic_dict = dict()
            topic_to_package_dict = dict()

            for package in package_topic_dict.keys():
                topic_list = package_topic_dict[package]
                formatted_package = package.lower()
                formatted_topic_list = [
                    GNOSIS_PTM_TOPIC_PREFIX + x.lower() for x in topic_list]
                distinct_formatted_topic_list = list(set(formatted_topic_list))
                package_to_topic_dict[
                    formatted_package] = distinct_formatted_topic_list

                for formatted_topic in distinct_formatted_topic_list:
                    if formatted_topic not in topic_to_package_dict:
                        topic_to_package_dict[
                            formatted_topic] = [formatted_package]
                    else:
                        temp_package_list = topic_to_package_dict[
                            formatted_topic]
                        topic_to_package_dict[
                            formatted_topic] = temp_package_list + [formatted_package]

            eco_to_package_to_topic_dict[ecosystem] = package_to_topic_dict
            eco_to_topic_to_package_dict[ecosystem] = topic_to_package_dict

        eco_to_package_topic_dict[
            GNOSIS_PTM_PACKAGE_TOPIC_MAP] = eco_to_package_to_topic_dict
        eco_to_package_topic_dict[
            GNOSIS_PTM_TOPIC_PACKAGE_MAP] = eco_to_topic_to_package_dict

        return GnosisPackageTopicModel(eco_to_package_topic_dict)

    def save(self, data_store, filename):
        """Save the Package Topic Model.

        :param data_store: destination Data store to store the model.
        :param file_name: Name of the file that will contain model."""

        data_store.write_json_file(
            filename=filename, contents=self.get_dictionary())

    @classmethod
    def load(cls, data_store, filename):
        """Load the Packag Topic Model.

        :param data_store: Data store to keep the model.
        :param file_name: Name of the file that contains model."""

        dictionary = data_store.read_json_file(filename)
        return GnosisPackageTopicModel(dictionary=dictionary)

    def get_dictionary(self):
        """gets the dictionary
        :return: a dict object"""

        return self._dictionary
