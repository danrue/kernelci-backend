# Copyright (C) 2014 Linaro Ltd.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""The model that represents a job document in the mongodb collection."""

from bson import json_util
from types import StringTypes

from models import (
    COMPILER_VERSION_KEY,
    CROSS_COMPILE_KEY,
    GIT_BRANCH_KEY,
    GIT_COMMIT_KEY,
    GIT_DESCRIBE_KEY,
    GIT_URL_KEY,
    ID_KEY,
    JOB_KEY,
    KERNEL_KEY,
    METADATA_KEY,
    PRIVATE_KEY,
    STATUS_KEY,
    UPDATED_KEY,
)
from models.base import BaseDocument

JOB_COLLECTION = 'job'


class JobDocument(BaseDocument):
    """This class represents a job as seen on the file system.

    Each job on the file system is composed of a real job name (usually who
    triggered the job), and a kernel directory. This job is the combination
    of the two, and its name is of the form `job-kernel`.
    """

    ID_FORMAT = '%(job)s-%(kernel)s'
    METADATA_KEYS = (
        CROSS_COMPILE_KEY, COMPILER_VERSION_KEY,
        GIT_URL_KEY, GIT_BRANCH_KEY, GIT_DESCRIBE_KEY, GIT_COMMIT_KEY,
    )

    def __init__(self, name, job=None, kernel=None):
        super(JobDocument, self).__init__(name)

        self._private = False
        self._job = job
        self._kernel = kernel
        self._status = None
        self._updated = None
        self._metadata = {}

    @property
    def collection(self):
        return JOB_COLLECTION

    @property
    def private(self):
        """If the job is private or not.

        :return True or False
        """
        return self._private

    @private.setter
    def private(self, value):
        """Set the private attribute."""
        self._private = value

    @property
    def job(self):
        """Return the real job name as found on the file system."""
        return self._job

    @job.setter
    def job(self, value):
        """Set the real job name as found on the file system."""
        self._job = value

    @property
    def kernel(self):
        """Return the real kernel name as found on the file system."""
        return self._kernel

    @kernel.setter
    def kernel(self, value):
        """Set the real kernel name as found on the file system."""
        self._kernel = value

    @property
    def updated(self):
        """The date this document was last updated.

        :return A string representing a datetime object in ISO format,
                UTC time zone.
        """
        return self._updated

    @updated.setter
    def updated(self, value):
        """Set the date this document was last updated.

        :param value: A string representing a datetime object in ISO format.
        """
        self._updated = value

    @property
    def status(self):
        """The build status of this job."""
        return self._status

    @status.setter
    def status(self, value):
        """Set the build status of the job.

        :param value: The status.
        """
        self._status = value

    @property
    def metadata(self):
        """The metadata associated with this job.

        A dictionary contaning information like commit ID, tree URL...
        """
        return self._metadata

    @metadata.setter
    def metadata(self, value):
        """Set the metadata dictionary associated with this job.

        :param value: A dictionary containing the metadata.
        """
        self._metadata = value

    def to_dict(self):
        job_dict = super(JobDocument, self).to_dict()
        job_dict[PRIVATE_KEY] = self._private
        job_dict[JOB_KEY] = self._job
        job_dict[KERNEL_KEY] = self._kernel
        job_dict[UPDATED_KEY] = self._updated
        job_dict[STATUS_KEY] = self._status
        job_dict[METADATA_KEY] = self._metadata
        return job_dict

    @staticmethod
    def from_json(json_obj):
        """Build a document from a JSON object.

        :param json_obj: The JSON object to start from, or a JSON string.
        :return An instance of `JobDocument`.
        """
        if isinstance(json_obj, StringTypes):
            json_obj = json_util.loads(json_obj)

        name = json_obj.pop(ID_KEY)

        job_doc = JobDocument(name)
        for key, value in json_obj.iteritems():
            setattr(job_doc, key, value)

        return job_doc
