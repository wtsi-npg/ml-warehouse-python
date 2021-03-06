# -*- coding: utf-8 -*-
#
# Copyright © 2021 Genome Research Ltd. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# @author Adam Blanchet <ab59@sanger.ac.uk>

from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from ml_warehouse.schema import FlgenPlate, OseqFlowcell, PacBioRun, Sample, Study


def get_recent_pacbio_runs(sess: Session, max_age: datetime):
    """Get recently updated Pacbio runs within a given timeframe.

    Arguments
    ---------
    sess: Session
        The Session to perform the search against.
    max_age: timedelta
        The maximum age of the PacBio runs.

    Returns
    -------
    Query
        The Query corresponding to the search.
    """

    return (
        sess.query(
            Sample.last_updated.label("sample_last_updated"),
            Study.last_updated.label("study_last_updated"),
            PacBioRun.last_updated.label("pacbiorun_last_updated"),
            PacBioRun.id_pac_bio_run_lims,
            PacBioRun.plate_barcode,
            PacBioRun.well_label,
            PacBioRun.pac_bio_library_tube_name,
            PacBioRun.tag_set_name,
            PacBioRun.tag_set_id_lims,
            PacBioRun.tag_sequence,
            PacBioRun.tag_identifier,
            PacBioRun.tag2_set_name,
            PacBioRun.tag2_sequence,
            PacBioRun.tag2_identifier,
        )
        .distinct()
        .join(PacBioRun.sample, PacBioRun.study)
        .filter((Sample.last_updated > max_age) | (Study.last_updated > max_age))
    )


def get_recent_ont(sess: Session, max_age: datetime):
    """Get recently updated OseqFlowcell within a given timeframe.

    Arguments
    ---------
    sess: Session
        The Session to perform the search against.
    max_age: time_delta
        The maximum age of the last update to the OseqFlowcell entry.

    Returns
    -------
    Query
        The Query corresponding to the search.
    """

    return (
        sess.query(
            Sample.name,
            Sample.supplier_name,
            Study.id_study_lims,
            OseqFlowcell.experiment_name,
            OseqFlowcell.instrument_slot,
            OseqFlowcell.tag_set_name,
            OseqFlowcell.tag_set_id_lims,
            OseqFlowcell.tag_sequence,
            OseqFlowcell.tag_identifier,
            OseqFlowcell.tag2_set_name,
            OseqFlowcell.tag2_sequence,
            OseqFlowcell.tag2_identifier,
        )
        .distinct()
        .join(OseqFlowcell.sample)
        .join(OseqFlowcell.study)
        .filter(
            (OseqFlowcell.last_updated > max_age)
            | (Sample.last_updated > max_age)
            | (Study.last_updated > max_age)
        )
    )


def get_recent_fluidigm(sess: Session, max_age: datetime):
    """Get recemt Fludigm details more recent than a certain age.

    Arguments
    ---------
    sess: Session
        The Session to perform the search against.
    max_age: timedelta
        The maximum age of the last update to the FlgenPlate's corresponding Sample.


    Returns
    -------
    Query
        The Query corresponding to the search, with fields `name`, `consent_withdrawn`,
        `last_updated`, `id_study_lims`, `plate_barcode`, `well_label` and `recorded_at`.
    """

    return (
        sess.query(
            Sample.name,
            Sample.consent_withdrawn,
            Sample.last_updated,
            Study.id_study_lims,
            FlgenPlate.plate_barcode,
            FlgenPlate.well_label,
            FlgenPlate.recorded_at,
        )
        .distinct()
        .join(FlgenPlate.sample)
        .join(FlgenPlate.study)
        .filter(
            (FlgenPlate.last_updated > max_age)
            | (Study.last_updated > max_age)
            | (Sample.last_updated > max_age)
        )
    )
