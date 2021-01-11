function bootstrapComponentAjaxCall( target, target_body ) {
    var fetch_url = target.attributes.getNamedItem('data-url').value;
    var tooltips = $('[data-toggle="tooltip"]', target);
    var spinner = $('.django-bootstrap-swt-spinner', target_body);
    var error = $('.django-bootstrap-swt-error', target_body);

    const modal = target.querySelector("div").closest(".modal")
    var fetched_content;
    if ( modal ){
        fetched_content = $('#id_' + modal.id + '_fetched_content');
    }

    tooltips.tooltip("hide");
    $.ajax({
      url: fetch_url,
      beforeSend: function() {
        spinner.removeClass("d-none");
        if ( modal ){
            fetched_content.html( "" );
        }
      },
      success: function( data ) {
        spinner.addClass("d-none");
        if ( fetched_content ){
            fetched_content.html( data );
        } else {
            target_body.html( data );
        }
        tooltips.tooltip();
        initAjaxComponents(target);
      },
      error: function() {
        spinner.addClass("d-none");
        error.removeClass("d-none");
      },
    });
}

function modalAjaxInit( parent ) {
    $(".modal[data-url]", parent).on('shown.bs.modal', function( event ) {
        bootstrapComponentAjaxCall( event.currentTarget, $( '.modal-content', event.currentTarget ) );
    });
}

function collapseAjaxInit( parent ) {
    $(".collapse[data-url]", parent).on('shown.bs.collapse', function( event ) {
        bootstrapComponentAjaxCall( event.target, $( event.target ) );
    });
}

function initAjaxComponents( parent ) {
    modalAjaxInit( parent );
    collapseAjaxInit( parent );
}

$( document ).ready( function(){
    initAjaxComponents( document );
});