"""
Web frontend for various scientific applications
Copyright (C) <2023>  <Normand Cyr>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from flask_wtf import FlaskForm

from flask_uploads import UploadSet, AllExcept, SCRIPTS, EXECUTABLES
from wtforms import RadioField, FileField, SubmitField
from wtforms.validators import InputRequired


from app import colour_maps

pim_file = UploadSet("pimfile", extensions=AllExcept(SCRIPTS + EXECUTABLES))


class SubmissionForm(FlaskForm):
    individual_cmaps = colour_maps.cmap_list
    file = FileField(
        label="Choose the file containing the percent identity matrix data:",
        validators=[InputRequired()],
    )
    colour_map = RadioField(
        label="Choose a colour map:",
        choices=individual_cmaps,
        default="Greys",
        validators=[InputRequired()],
    )
    submit = SubmitField("Generate")
