$("#id_question_type").change(function(){
    // alert("The text has been changed.");
    // $('#id_question_type').val(parameter)
    seleted_option = $(this).val();
    objective_block = $('#objective');
    attachment_block = $('#attachment');
    descriptive_block = $('#descriptive');
    descriptive_or_file_block = $('#descriptive_or_file');

    objective_block.addClass('d-none');
    attachment_block.addClass('d-none');
    descriptive_block.addClass('d-none');

    console.log(seleted_option);
    if(seleted_option == 'objective'){
        objective_block.removeClass('d-none');
    }
    if(seleted_option == 'attachment'){
        attachment_block.removeClass('d-none');
    }
    if(seleted_option == 'descriptive'){
        descriptive_block.removeClass('d-none');
    }
    if(seleted_option == 'descriptive_or_file'){
        attachment_block.removeClass('d-none');
    }
  });