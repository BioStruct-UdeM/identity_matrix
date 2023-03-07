from flask_wtf import FlaskForm
from wtforms import RadioField, FileField, SubmitField
from wtforms.validators import DataRequired

from app import colour_maps


class SubmissionForm(FlaskForm):
    individual_cmaps = colour_maps.cmap_list
    file = FileField(
        label="Choose the file containing the percent identity matrix data:",
        validators=[DataRequired()],
    )
    colour_map = RadioField(
        label="Choose a colour map:",
        choices=individual_cmaps,
        default="Greys",
        validators=[DataRequired()],
    )
    submit = SubmitField("Generate")
