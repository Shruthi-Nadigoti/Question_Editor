## User Interface for Editing Questions

   In pybossa we do not have User Interface for Editing questions.We need to write the questions in google
   spreadsheet or CSV file.If the questions are same for a perticular category like images, videos, documents 
   and audios.Then we have to copy the question for all the tasks which are in the same category.If the user want 
   to upload tasks in bulk amount then she/he should write the questions for all. So by considering all these 
   issues, this module has been made.
   
   You can write the common questions for each perticular category like images, documents, videos and audios. 
   You can perform All CRUD(create, read, update, delete) operations in this interface.You can skip the category 
   if do not have perticular category.
   
## Installation
   - Clone this repository add rename it to **question_editor** and paste it in pybossa/pybossa/plugins
   - Insert the below lines of code in if condition of pybossa/pybossa/themes/default/templates/projects/tasks.html file
   
   ```
    <div class="row">
        <div id="task_browse" class="col-md-6">
        {{ render_project_card_option(project, upload_method, title=_('Editing Questions'), explanation=_('Edit the questions for tasks'), link=url_for('question_editor.edit_question', short_name=project.short_name), link_action_text=_('Edit Questions'), icon='compass')}}
        </div>
    </div>
   ```
   - Now can able to see the **Editing Questions** in the cards.
 
## Steps to Edit the Questions

   **Note** : You can edit the questions when the project is in the only draft stage.
   * Click in the **Tasks** link which is on the left side local navigation menu.
   * Choose the **Editing Questions** cart. And click on the Edit questions.
   * Now you can do CRUD (create, read , update ,delete) operations on those questions.
   * Click on **submit** to save the changes.
   
