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
