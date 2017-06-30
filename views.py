#from pybossa.view.projects import blueprint
from flask import Blueprint,request,Response,render_template,redirect,flash,current_app,url_for,session
from pybossa.util import (Pagination, admin_required, get_user_id_or_ip, rank,
                          handle_content_type, redirect_content_type,
                          get_avatar_url)
from flask.ext.login import login_required, current_user
from pybossa.view.projects import sanitize_project_owner,project_by_shortname,pro_features
from pybossa.cache.helpers import add_custom_contrib_button_to
import json
from pybossa.core import project_repo
from pybossa.pro_features import ProFeatureHandler


blueprint = Blueprint('question_editor', __name__,template_folder='templates',static_folder="static")

@blueprint.route('/<short_name>/tasks/edit_question',methods=['GET', 'POST'])
@login_required
def edit_question(short_name):
    (project, owner, n_tasks, n_task_runs,
     overall_progress, last_activity,
     n_results) = project_by_shortname(short_name)
    pro=pro_features()
    project_button = add_custom_contrib_button_to(project, get_user_id_or_ip())
    feature_handler = ProFeatureHandler(current_app.config.get('PRO_FEATURES'))
    autoimporter_enabled = feature_handler.autoimporter_enabled_for(current_user)
    project_sanitized, owner_sanitized = sanitize_project_owner(project_button, owner, current_user)
    print project_button["contrib_button"]
    if(project_button["contrib_button"]=="draft"):
        if("questionSet" not in project.info.keys()):
            project.info.update({"questionSet":{"images":[],"videos":[],"audios":[],"documents":[]}})
            project_repo.update(project)

        session["edit_question"]={"images":[],"documents":[],"videos":[],"audios":[]}
        return redirect_content_type(url_for('.images_edit',short_name=short_name))

    else:
        return ("Sorry, You Edit the questions for draft project only.","alert")

@blueprint.route('/<short_name>/tasks/test', methods=['GET', 'POST'])
@login_required
def test(short_name):
    return short_name

@blueprint.route('/<short_name>/tasks/edit_success', methods=['GET', 'POST'])
@login_required
def edit_success(short_name):
    (project, owner, n_tasks, n_task_runs,
     overall_progress, last_activity,
     n_results) = project_by_shortname(short_name)
    pro=pro_features()
    project_button = add_custom_contrib_button_to(project, get_user_id_or_ip())
    feature_handler = ProFeatureHandler(current_app.config.get('PRO_FEATURES'))
    autoimporter_enabled = feature_handler.autoimporter_enabled_for(current_user)
    project_sanitized, owner_sanitized = sanitize_project_owner(project_button, owner, current_user)
    return  render_template('edit_success.html',project=project_sanitized,
    pro_features=pro) #we are going to tags.html


@blueprint.route('/<short_name>/tasks/images_edit', methods=['GET', 'POST'])
@login_required
def images_edit(short_name):
    (project, owner, n_tasks, n_task_runs,
     overall_progress, last_activity,
     n_results) = project_by_shortname(short_name)
    pro=pro_features()
    project_button = add_custom_contrib_button_to(project, get_user_id_or_ip())
    feature_handler = ProFeatureHandler(current_app.config.get('PRO_FEATURES'))
    autoimporter_enabled = feature_handler.autoimporter_enabled_for(current_user)
    project_sanitized, owner_sanitized = sanitize_project_owner(project_button, owner, current_user)
    if request.method == 'POST':
        session_count=len(session["edit_question"]["images"]);
        session["edit_question"]["images"]=[]
        for j in range(1,session_count+1):
            ans=[]
            type_q="normal"
            print str(j)+'_question'
            if(request.form.get(str(j)+'_question','')!=""):
                que=request.form.get(str(j)+'_question')
                if(request.form.get(str(j)+'_divcheckbox','')!=""):
                    type_q="mcqs"
                    if(request.form.get(str(j)+'_answer','')!=""):
                        ans=request.form.getlist(str(j)+'_answer')

                dictobj={"questionString":request.form.get(str(j)+'_question'),"answers":ans,"type":type_q}
                session["edit_question"]["images"].append(dictobj)

        if(request.form.get('submit','')=="submit"):
            project.info["questionSet"]["images"]=session["edit_question"]["images"]
            project_repo.update(project)
            if(len(session["edit_question"]["images"])==0):
                flash("You have not added any questions for the images","warning")
            return redirect_content_type(url_for('.documents_edit',short_name=short_name))
        else:
            type_q="normal"
            answer=[]
            if(request.form.get('question','')==""):
                flash("Question field is Empty","warning")
                return  render_template('images_edit.html',project=project_sanitized,
                pro_features=pro)
            if(request.form.get('checkbox','')!=""):
                if(request.form.getlist('answer')[0]=="" or request.form.getlist('answer')[1]==""):
                    flash("Atleast 2 answers are required","warning")
                    return  render_template('images_edit.html',project=project_sanitized,
                    pro_features=pro)
                else:
                    type_q="mcqs"
                    answer=request.form.getlist('answer')
            dictobj={"questionString":request.form.get('question'),"answers":answer,"type":type_q}
            session["edit_question"]["images"].append(dictobj)

    return  render_template('images_edit.html',project=project_sanitized,pro_features=pro) #we are going to tags.html

@blueprint.route('/<short_name>/tasks/documents_edit', methods=['GET', 'POST'])
@login_required
def documents_edit(short_name):
    (project, owner, n_tasks, n_task_runs,
     overall_progress, last_activity,
     n_results) = project_by_shortname(short_name)
    pro=pro_features()
    project_button = add_custom_contrib_button_to(project, get_user_id_or_ip())
    feature_handler = ProFeatureHandler(current_app.config.get('PRO_FEATURES'))
    autoimporter_enabled = feature_handler.autoimporter_enabled_for(current_user)
    project_sanitized, owner_sanitized = sanitize_project_owner(project_button, owner, current_user)
    if request.method == 'POST':
        session_count=len(session["edit_question"]["documents"]);
        session["edit_question"]["documents"]=[]
        for j in range(1,session_count+1):
            ans=[]
            type_q="normal"
            print str(j)+'_question'
            if(request.form.get(str(j)+'_question','')!=""):
                que=request.form.get(str(j)+'_question')
                if(request.form.get(str(j)+'_divcheckbox','')!=""):
                    type_q="mcqs"
                    if(request.form.get(str(j)+'_answer','')!=""):
                        ans=request.form.getlist(str(j)+'_answer')

                dictobj={"questionString":request.form.get(str(j)+'_question'),"answers":ans,"type":type_q}
                session["edit_question"]["documents"].append(dictobj)

        if(request.form.get('submit','')=="submit"):
            #p=edit_draft_question(project)
            project.info["questionSet"]["documents"]=session["edit_question"]["documents"]
            project_repo.update(project)
            if(len(session["edit_question"]["documents"])==0):
                flash("You have not added any questions for the documents","warning")
            return redirect_content_type(url_for('.videos_edit',short_name=short_name))
        else:
            type_q="normal"
            answer=[]
            if(request.form.get('question','')==""):
                flash("Question field is Empty","warning")
                return  render_template('documents_edit.html',project=project_sanitized,
                pro_features=pro)
            if(request.form.get('checkbox','')!=""):
                if(request.form.getlist('answer')[0]=="" or request.form.getlist('answer')[1]==""):
                    flash("Atleast 2 answers are required","warning")
                    return  render_template('documents_edit.html',project=project_sanitized,
                    pro_features=pro)
                else:
                    type_q="mcqs"
                    answer=request.form.getlist('answer')
            dictobj={"questionString":request.form.get('question'),"answers":answer,"type":type_q}
            session["edit_question"]["documents"].append(dictobj)

    return  render_template('documents_edit.html',project=project_sanitized,pro_features=pro) #we are going to tags.html


@blueprint.route('/<short_name>/tasks/videos_edit', methods=['GET', 'POST'])
@login_required
def videos_edit(short_name):
    (project, owner, n_tasks, n_task_runs,
     overall_progress, last_activity,
     n_results) = project_by_shortname(short_name)
    pro=pro_features()
    project_button = add_custom_contrib_button_to(project, get_user_id_or_ip())
    feature_handler = ProFeatureHandler(current_app.config.get('PRO_FEATURES'))
    autoimporter_enabled = feature_handler.autoimporter_enabled_for(current_user)
    project_sanitized, owner_sanitized = sanitize_project_owner(project_button, owner, current_user)
    if request.method == 'POST':
        session_count=len(session["edit_question"]["videos"]);
        session["edit_question"]["videos"]=[]
        for j in range(1,session_count+1):
            ans=[]
            type_q="normal"
            print str(j)+'_question'
            if(request.form.get(str(j)+'_question','')!=""):
                que=request.form.get(str(j)+'_question')
                if(request.form.get(str(j)+'_divcheckbox','')!=""):
                    type_q="mcqs"
                    if(request.form.get(str(j)+'_answer','')!=""):
                        ans=request.form.getlist(str(j)+'_answer')

                dictobj={"questionString":request.form.get(str(j)+'_question'),"answers":ans,"type":type_q}
                session["edit_question"]["videos"].append(dictobj)

        if(request.form.get('submit','')=="submit"):
            #p=edit_draft_question(project)
            project.info["questionSet"]["videos"]=session["edit_question"]["videos"]
            project_repo.update(project)
            if(len(session["edit_question"]["videos"])==0):
                flash("You have not added any questions for the videos","warning")
            return redirect_content_type(url_for('.audios_edit',short_name=short_name))
        else:
            type_q="normal"
            answer=[]
            if(request.form.get('question','')==""):
                flash("Question field is Empty","warning")
                return  render_template('videos_edit.html',project=project_sanitized,
                pro_features=pro)
            if(request.form.get('checkbox','')!=""):
                if(request.form.getlist('answer')[0]=="" or request.form.getlist('answer')[1]==""):
                    flash("Atleast 2 answers are required","warning")
                    return  render_template('videos_edit.html',project=project_sanitized,
                    pro_features=pro)
                else:
                    type_q="mcqs"
                    answer=request.form.getlist('answer')
            dictobj={"questionString":request.form.get('question'),"answers":answer,"type":type_q}
            session["edit_question"]["videos"].append(dictobj)

    return  render_template('videos_edit.html',project=project_sanitized,pro_features=pro) #we are going to tags.html

@blueprint.route('/<short_name>/tasks/audios_edit', methods=['GET', 'POST'])
@login_required
def audios_edit(short_name):
    (project, owner, n_tasks, n_task_runs,
     overall_progress, last_activity,
     n_results) = project_by_shortname(short_name)
    pro=pro_features()
    project_button = add_custom_contrib_button_to(project, get_user_id_or_ip())
    feature_handler = ProFeatureHandler(current_app.config.get('PRO_FEATURES'))
    autoimporter_enabled = feature_handler.autoimporter_enabled_for(current_user)
    project_sanitized, owner_sanitized = sanitize_project_owner(project_button, owner, current_user)
    if request.method == 'POST':
        session_count=len(session["edit_question"]["audios"]);
        session["edit_question"]["audios"]=[]
        for j in range(1,session_count+1):
            ans=[]
            type_q="normal"
            print str(j)+'_question'
            if(request.form.get(str(j)+'_question','')!=""):
                que=request.form.get(str(j)+'_question')
                if(request.form.get(str(j)+'_divcheckbox','')!=""):
                    type_q="mcqs"
                    if(request.form.get(str(j)+'_answer','')!=""):
                        ans=request.form.getlist(str(j)+'_answer')

                dictobj={"questionString":request.form.get(str(j)+'_question'),"answers":ans,"type":type_q}
                session["edit_question"]["audios"].append(dictobj)

        if(request.form.get('submit','')=="submit"):
            project.info["questionSet"]["audios"]=session["edit_question"]["audios"]
            project_repo.update(project)
            if(len(session["edit_question"]["audios"])==0):
                flash("You have not added any questions for the audios","warning")
            return redirect_content_type(url_for('.edit_success',short_name=short_name))
        else:
            type_q="normal"
            answer=[]
            if(request.form.get('question','')==""):
                flash("Question field is Empty","warning")
                return  render_template('audios_edit.html',project=project_sanitized,
                pro_features=pro)
            if(request.form.get('checkbox','')!=""):
                if(request.form.getlist('answer')[0]=="" or request.form.getlist('answer')[1]==""):
                    flash("Atleast 2 answers are required","warning")
                    return  render_template('audios_edit.html',project=project_sanitized,
                    pro_features=pro)
                else:
                    type_q="mcqs"
                    answer=request.form.getlist('answer')
            dictobj={"questionString":request.form.get('question'),"answers":answer,"type":type_q}
            session["edit_question"]["audios"].append(dictobj)

    return  render_template('audios_edit.html',project=project_sanitized,pro_features=pro) #we are going to tags.html
