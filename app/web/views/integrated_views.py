import json
from flask import Blueprint, g, jsonify, request
import os
from app.mcp_jira.mcp_utils import (
    create_jira_issue_mcp,
    search_jira_issues_mcp,
    get_jira_issue_mcp,
    add_jira_comment_mcp,
    get_jira_projects_mcp
)

bp = Blueprint('integrated', __name__, url_prefix='/api/integration')

@bp.route("/jira", methods=["POST"])
def create_jira():
    """Create Jira issue using MCP client"""
    try:
        payload = request.get_json()
        ticket_text = payload["ticket"]
        
        # Create the issue using MCP utility
        result = create_jira_issue_mcp(ticket_text)
        
        return jsonify({
            "message": "Story created successfully via MCP!",
            "data": result
        }), 201
        
    except Exception as e:
        return jsonify({
            "message": "Failed to create story via MCP",
            "error": str(e)
        }), 500

@bp.route("/jira/search", methods=["POST"])
def search_jira():
    """Search Jira issues using MCP client"""
    try:
        payload = request.get_json()
        jql = payload.get("jql", "project = EP")
        max_results = payload.get("max_results", 50)
        
        result = search_jira_issues_mcp(jql, max_results)
        
        return jsonify({
            "message": "Search completed successfully",
            "data": result
        }), 200
        
    except Exception as e:
        return jsonify({
            "message": "Failed to search issues",
            "error": str(e)
        }), 500

@bp.route("/jira/issue/<issue_key>", methods=["GET"])
def get_jira_issue(issue_key):
    """Get Jira issue details using MCP client"""
    try:
        result = get_jira_issue_mcp(issue_key)
        
        return jsonify({
            "message": "Issue retrieved successfully",
            "data": result
        }), 200
        
    except Exception as e:
        return jsonify({
            "message": "Failed to get issue",
            "error": str(e)
        }), 500

@bp.route("/jira/issue/<issue_key>/comment", methods=["POST"])
def add_jira_comment(issue_key):
    """Add comment to Jira issue using MCP client"""
    try:
        payload = request.get_json()
        comment = payload.get("comment", "")
        
        result = add_jira_comment_mcp(issue_key, comment)
        
        return jsonify({
            "message": "Comment added successfully",
            "data": result
        }), 200
        
    except Exception as e:
        return jsonify({
            "message": "Failed to add comment",
            "error": str(e)
        }), 500

@bp.route("/jira/projects", methods=["GET"])
def get_jira_projects():
    """Get available Jira projects using MCP client"""
    try:
        result = get_jira_projects_mcp()
        
        return jsonify({
            "message": "Projects retrieved successfully",
            "data": result
        }), 200
        
    except Exception as e:
        return jsonify({
            "message": "Failed to get projects",
            "error": str(e)
        }), 500
