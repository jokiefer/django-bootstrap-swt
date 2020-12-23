QUnit.module('django-bootstrap-swt', {
    beforeEach: function(assert) {
        $.ajax({
            url : "modal.html",
            dataType: "html",
            success : function (data) {
                $("#qunit-fixture").html(data);
            }
        });

        assert.ok($('#id_modal'))
        assert.ok($('#id_modal_body'))

        //$.ajax = function(options) {
        //    equals(options.url, "Http://example.com");
        //    options.success("Hello");
        //};
    }
});

QUnit.test("bootstrapComponentAjaxCall adds response content to target_body", function(assert) {

    var done = assert.async();
    setTimeout(function() {
        assert.ok(true);
        done();
    }, 1000);

    initAjaxComponents( document );
    bootstrapComponentAjaxCall( $('#id_modal'), $('#id_modal_body'))
    // $('#id_modal').modal('show')

    var done2 = assert.async();
    setTimeout(function() {
       assert.ok($('#id_modal').hasClass('show'));
       assert.equal($('#id_modal_body').text(), 'Hello');
       // Tell QUnit to wait for the done() call inside the timeout.
       done2();
    }, 1000);

});
