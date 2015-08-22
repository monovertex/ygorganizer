

define([
    'backbone.paginator',
    'model/card-version',
    'underscore'
], function (PageableCollection, CardVersion, _) {

    return function (url) {
        return PageableCollection.extend({

            model: CardVersion,

            url: url,

            mode: 'server',

            state: {
                firstPage: 0,
                currentPage: 0,
                pageSize: 30
            },

            fetch: function () {
                var promise = PageableCollection.prototype.fetch
                    .apply(this, arguments);

                promise.done(_.bind(function (result) {
                    this.statistics = result[0];
                    this.trigger('fetched', this.statistics);
                }, this));

                return promise;
            }

        });
    };

});