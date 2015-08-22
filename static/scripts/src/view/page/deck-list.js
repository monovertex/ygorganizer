

define([
    'backbone',
    'jquery',
    'underscore',
    'view/component/confirm'
], function (Backbone, $, _, Confirm) {

    return Backbone.View.extend({

        el: '#content.page-decks',

        events: {
            'click .delete': 'delete'
        },

        delete: function (ev) {
            var $button = $(ev.currentTarget),
                deckId = $button.data('deck'),
                $deck = $button.parents('.deck-wrapper');

            Confirm.ask().done(_.bind(function () {
                $.ajax({
                    method: 'delete',
                    url: '/api/decks/' + deckId + '/',
                }).done(function () {
                    $deck.fadeOut();
                });
            }, this));

            return false;
        }

    });

});