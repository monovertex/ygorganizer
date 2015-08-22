
define(['underscore', 'backbone'],
function (_, Backbone, config) {

    return Backbone.View.extend({

        initialize: function (options) {
            _.bindAll(this, 'render');

            this.template = this.template || options.template;

            this.listenTo(this.model, 'change', this.render);
        },

        render: function () {
            this.$el.html(this.template(this.model.attributes));

            this.delegateEvents();

            return this;
        }

    });

});