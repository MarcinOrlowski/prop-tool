"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""

from .check import Check
from ..config import Config
from ..overrides import overrides
from ..report.report_group import ReportGroup


# #################################################################################################

# noinspection PyUnresolvedReferences
class MissingKeys(Check):
    @staticmethod
    @overrides(Check)
    # Do NOT "fix" the PropFile reference and do not import it, or you step on circular dependency!
    def check(config: Config, reference_file: 'PropFile', translation_file: 'PropFile' = None) -> ReportGroup:

        report = ReportGroup('Missing keys')

        my_keys = translation_file.keys.copy()
        missing_keys: List[str] = []

        # Check if we have all reference keys present.
        for key in reference_file.keys:
            if key in my_keys:
                my_keys.remove(key)
            else:
                missing_keys.append(key)

        # Commented out keys are also considered present in the translation unless
        # we run in strict check mode.
        if not config.strict:
            commented_out_keys = translation_file.commented_out_keys.copy()
            for key in commented_out_keys:
                if key in missing_keys:
                    missing_keys.remove(key)

        for key in missing_keys:
            report.error(key)

        return report
