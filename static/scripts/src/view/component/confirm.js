

define([
    'underscore',
    'backbone',
    'jquery',
    'bootstrap'
], function (_, Backbone, $) {

    return new (Backbone.View.extend({

        el: '#confirm-modal',

        events: {
            'click .yes': 'yes',
            'click .no': 'no'
        },

        initialize: function () {
            this.promises = [];

            this.$el.modal({
                backdrop: 'static',
                show: false
            });
        },

        ask: function () {
            var promise = $.Deferred();

            this.promises.push(promise);

            this.$el.modal('show');

            return promise;
        },

        close: function () {
            this.promises = [];

            this.$el.modal('hide');
        },

        yes: function () {
            _.each(this.promises, function (promise) {
                promise.resolve();
            });
            this.close();
        },

        no: function () {
            _.each(this.promises, function (promise) {
                promise.reject();
            });
            this.close();
        }

    })) ();

});