$(function() {
  // Comment Entry
  $('#comment_entry').click(function() {
    commentEntryModel(base.detail.actions.comment, 1);
    commentSaveDone = function(data) {
      showAlertModal('info', data.message);
    };
  });
  $('#comment_confirm').click(function() {
    commentConfirm();
  });
  $('#comment_save').click(function() {
    commentSave();
  });
  $('#comment_back').click(function() {
    commentEntry();
  });

  // Comment Reply
  $('.comment-reply').click(function() {
    var $comment = cloneComment($(this).closest('.comment'));
    $('#comment_modal .comment-wrapper').empty().append($comment);
    var action = base.actions.reply.replace(/\/0\//, f('/{0}/', $comment.data('id')));
    commentEntryModel(action, 2);
    commentSaveDone = function(data) {
      redirect(20, data.message);
    };
  });

  $('#comment_text').keydown(commentLength).blur(commentLength);

  // Comment Edit
  var $commentEdit;
  $('.comment-edit').click(function() {
    $commentEdit = $(this).closest('.comment');
    var $comment = cloneComment($commentEdit);
    var action = base.actions.comment_update.replace(/\/0\//, f('/{0}/', $comment.data('id')));
    $('#comment_edit_form').attr('action', action);
    $('#comment_edit_modal .comment-wrapper').empty().append($comment);
    $('#comment_edit_form select[name="status"]').val($comment.data('status'));
    $('#comment_edit_modal').modal('show');
  });
  $('#comment_update').click(function() {
    commentUpdate($commentEdit);
  });

  // Code Clipboard
  initClipboard('.clipboard', {
    text: function(trigger) {
      return $.trim($(trigger).closest('.code-content').find('code').text());
    }
  });

  // Code Popup
  var $modal = $('#code_modal');
  $('.popup').click(function() {
    var $codeContent = $(this).closest('.code-content');
    var $pre = $codeContent.find('pre').clone();
    $modal.find('.modal-title').text($codeContent.find('.code-title').text());
    $modal.find('.code-body').empty().append($pre);
    $modal.modal('show');
  }).attr('data-original-title', 'Show with modal').tooltip();
  initClipboard('#code_modal_clipboard', {
    container: $modal[0],
    text: function(trigger) {
      return $.trim($(trigger).closest('.code-content').find('code').text());
    }
  });
});

function initClipboard(selector, options) {
    new ClipboardJS(selector, options).on('success', function(e) {
      showTooltip($(e.trigger), 'Copied!');
      e.clearSelection();
    }).on('error', function(e) {
      showTooltip($(e.trigger), 'Error!');
      e.clearSelection();
    });
    $(selector).attr('data-original-title', 'Copy to clipboard').tooltip();
}
function showTooltip($target, msg) {
  var original = $target.attr('data-original-title');
  $target.attr('data-original-title', msg).tooltip('show').attr('data-original-title', original);
}

function commentLength() {
  var length = $(this).val().length;
  $('#comment_length').text(length);
  $('#comment_confirm').prop('disabled', !length);
}
function cloneComment($comment) {
  var $clone = $comment.clone();
  $clone.data('id', $comment.data('id'));
  $clone.data('status', $comment.data('status'));
  $clone.find('.comment-edit').parent().remove();
  $clone.find('.reply-container').remove();
  return $clone;
}
function commentEntryModel(action, mode) {
  var $modal = $('#comment_modal');
  $modal.find('form').attr('action', action);
  $modal.find('.alert-container').empty();
  $modal.find('.modal-title').text(mode == 1? base.detail.messages['Comment Entry'] : base.detail.messages['Reply Entry']);
  $modal.find('.comment-wrapper').toggle(mode != 1);
  $modal.find('.comment-note').toggle(mode == 1);
  $modal.modal('show');
  commentEntry();
  $('#name_text,#comment_text').val('');
}
function commentEntry() {
  $('#comment_modal_message').text(base.detail.messages['COMMENT_ENTRY']);
  enabled($('#name_text,#comment_text'), true);
  $('#comment_confirm').show();
  $('#comment_back,#comment_save').hide();
  $('#comment_text').focus();
}
function commentConfirm() {
  $('#comment_modal .alert-container').empty();
  $('#comment_modal_message').text(base.detail.messages['COMMENT_CONFIRM']);
  enabled($('#name_text,#comment_text'), false);
  $('#comment_confirm').hide();
  $('#comment_back,#comment_save').show();
}
var commentSaveDone;
function commentSave() {
  requestByForm($('#comment_form'),
    function(data, textStatus, jqXHR) {
      if (data.status == 1) {
        $('#comment_modal').modal('hide');
        commentSaveDone(data);
      } else {
        commentEntry();
        showAlert('error', data.message, $('#comment_modal .alert-container').empty());
      }
    }
  );
}

// Comment Edit
function commentUpdate($comment) {
  requestByForm($('#comment_edit_form'),
    function(data, textStatus, jqXHR) {
      if (data.status == 1) {
        showAlertModal('info', data.message);
        $comment.data('status', data.data.status);
        $comment.find('.comment-status').text(data.data.status_name);
      } else {
        showAlertModal('error', data.message);
      }
      $('#comment_edit_modal').modal('hide');
    }
  );
}

function enabled($targets, flag) {
  $targets.toggleClass('form-control', flag)
    .toggleClass('form-control-plaintext', !flag)
    .prop('readonly', !flag);
}