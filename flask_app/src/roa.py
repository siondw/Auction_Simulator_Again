from flask import Blueprint, request, jsonify, make_response, current_app
from Model.League import League, RoundOfAuction
import json

roa = Blueprint('roa', __name__)