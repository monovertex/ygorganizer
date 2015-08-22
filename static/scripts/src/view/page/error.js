

define([
    'backbone',
    'templates'
], function (Backbone, Templates) {

    return Backbone.View.extend({

        className: 'container error-page',

        template: Templates.error,

        initialize: function () {
            this.$el.html(this.template());
        },

        render: function () {
            return this;
        }

    });

});