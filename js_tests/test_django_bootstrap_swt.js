var data_url;

QUnit.module('django-bootstrap-swt', {
    beforeEach: function() {
        $.ajax({
            type: "GET",
            url : "modal.html",
            dataType: "html",
            async: false,
            success : function (data) {
                $("#qunit-fixture").html(data);
            }
        });
        data_url = $( "#id_modal" )[0].attributes.getNamedItem('data-url');
    }
});

QUnit.test("bootstrapComponentAjaxCall adds response content to target_body", function(assert) {
    data_url.value = "modal-content.html"
    var modal = $( "#id_modal" );
    var body = $('#id_modal_body');

    bootstrapComponentAjaxCall( modal[0], body )

    var done = assert.async();
    setTimeout(function() {
       assert.equal(body.text(), 'Hello');
       // Tell QUnit to wait for the done() call inside the timeout.
       done();
    }, 1000);
});

QUnit.test("bootstrapComponentAjaxCall adds response content to target_body", function(assert) {
    // if we don't set a value the test will run endless
    data_url.value = "something"
    var modal = $( "#id_modal" );
    var body = $('#id_modal_body');

    bootstrapComponentAjaxCall( modal[0], body )

    var done = assert.async();
    setTimeout(function() {
       assert.notOk($('.django-bootstrap-swt-error').hasClass("d-none"));
       // Tell QUnit to wait for the done() call inside the timeout.
       done();
    }, 1000);
});
