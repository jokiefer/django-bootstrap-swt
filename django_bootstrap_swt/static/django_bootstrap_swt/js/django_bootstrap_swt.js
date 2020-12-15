function bootstrapComponentAjaxCall( target, target_body ) {
    var fetch_url = target.attributes.getNamedItem('data-url').value;
    var tooltips = $('[data-toggle="tooltip"]', target);

    tooltips.tooltip("hide");
    target_body.html( `{% include 'django_bootstrap_swt/includes/ajax_loading_spinner.html' %}` );

    $.ajax({
      url: fetch_url,
      success: function( data ) {
        target_body.html( data );
        tooltips.tooltip();
        initAjaxComponents(target);
      },
      error: function() {
        target_body.html( `{% include 'django_bootstrap_swt/includes/ajax_error.html' %}` );
      },
    });
}

function modalAjaxInit( parent ) {
    $(".modal[data-url]", parent).on('shown.bs.modal', function( event ) {
        bootstrapComponentAjaxCall(event.currentTarget, $('.modal-body', event.currentTarget));
    });
}

function collapseAjaxInit( parent ) {
    $(".collapse[data-url]", parent).on('shown.bs.collapse', function( event ) {
        bootstrapComponentAjaxCall(event.target, $('.card-body', event.target));
    });
}

function initAjaxComponents( parent ) {
    modalAjaxInit(parent);
    collapseAjaxInit(parent);
}

$( document ).ready( function(){
    initAjaxComponents( document );
});