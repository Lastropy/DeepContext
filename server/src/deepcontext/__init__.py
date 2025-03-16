from flask import Flask
app = Flask(__name__)
import deepcontext.providers.main
import deepcontext.api.main