$(function(){
    $('[name=keyword]').keydown(function() {
        if (event.keyCode == 13) {
            search($(this).val());
        }
    });
    $('#search').click(function() {
        search($('#search-keyword').val());
    });
    $('.category').click(function() {
        var categoryText = $(this).data('category-text');
        if (categoryText.match(/ /))
            categoryText = '"' + categoryText + '"';
        search('category:' + categoryText);
    });
    $('.page-link').click(function() {
        $('#page').val($(this).data('page'));
        submit($(this).closest('form'));
    });
});

function search(keyword) {
    keyword = $.trim(keyword);
    if (!keyword)
        return;
    var $searchInput = $('#header-search').val(keyword);
    submit($searchInput.closest('form'));
}
function assign(url) {
    location.assign(url);
}
function submit($form) {
    $form.submit();
}

function requestByForm($form, done, fail, always) {
    request({
        url: $form.prop('action'),
        method: $form.prop('method'),
        data: $form.serialize(),
        timeout: 10000,
        dataType: 'json',
    }, done, fail, always);
}

function request(ajax, done, fail, always) {
    showLoading();
    $.ajax(ajax)
    .done(function(data, textStatus, jqXHR) {
        hideLoading();
        done && done(data, textStatus, jqXHR);
    })
    .fail(function(jqXHR, textStatus, errorThrown) {
        hideLoading();
        if (fail) {
            fail(jqXHR, textStatus, errorThrown);
        } else {
            systemError(jqXHR.status);
        }
    })
    .always(function() {
        always && always();
    });
}

function showLoading() {
    $('#overlay').show();
}
function hideLoading() {
    $('#overlay').hide();
}
function systemError(status) {
    redirect(40, 'System Error');
}
function redirect(level, message) {
    location.href = f('{0}?{1}', base.redirect_url, $.param({
        url: location.href,
        message_level: level,
        message: message
    }));
}

function showAlertHeader(type, message) {
    showAlert(type, message, $('#alert_container'));
    $('body, html').scrollTop(0);
}
function showAlertModal(type, message) {
    var $modal = $('#alert_modal');
    showAlert(type, message, $modal.find('.alert_container').empty()).find('.close').remove();
    $modal.modal();
}
function showAlert(type, message, $parent) {
    var $alert = $('#default_alert').clone().removeAttr('id');
    $alert.toggleClass('alert-info', type == 'info');
    $alert.toggleClass('alert-warning', type == 'warning');
    $alert.toggleClass('alert-danger', type == 'error');
    $alert.find('.message-text').text(message);
    $alert.appendTo($parent).show();
    return $alert;
}

// utility
function format(value) {
    if (arguments.length > 1) {
        var replaces = [].slice.call(arguments).slice(1, arguments.length);
        $.each(replaces, function(i, r) {value = value.replace('{' + i + '}', r);});
    }
    return value;
}
function trim(text) {
    return text.replace(/^[\s　]+|[\s　]+$/g, '');
}
function f(str) {
    if (arguments.length > 1) {
        var replaces = [].slice.call(arguments).slice(1, arguments.length);
        $.each(replaces, function(i, r) {str = str.replace('{' + i + '}', r);});
    }
    return str;
}