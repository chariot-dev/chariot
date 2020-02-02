from flask import Flask, request, app, jsonify, request

from chariot.database.Database import Database

DatabaseBaseUrl: str = '/chariot/api/v1.0/Database'
