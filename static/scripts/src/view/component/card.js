

define([
    'underscore',
    'backbone',
    'templates',
    'model/card'
], function (_, Backbone, Templates, Card) {

    return Backbone.View.extend({

        template: Templates.card,

        initialize: function (options) {
            _.bindAll(this);

            this.rootUrl = options.rootUrl;
        },

        render: function (identifier) {
            this.model = Card.findOrCreate({ identifier: identifier });

            if (this.model.get('image')) {
                this.renderCore();
            } else {
                this.model.fetch().done(this.renderCore);
            }
        },

        renderCore: function () {
            this.$el
                .html(this.template(_.extend({
                    rootUrl: this.rootUrl
                }, this.model.attributes)))
                .addClass('open');
        },

        hide: function () {
            this.$el.removeClass('open');
        }

    });

});