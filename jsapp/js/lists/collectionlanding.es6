import React from 'react/addons';
import Reflux from 'reflux';
import {Navigation} from 'react-router';
import Dropzone from '../libs/dropzone';
import assign from 'react/lib/Object.assign';

import {dataInterface} from '../dataInterface'
import searches from '../searches';
import actions from '../actions';
import mixins from '../mixins';
import stores from '../stores';
import bem from '../bem';
import ui from '../ui';

import AssetRow from '../components/assetrow';
import {List, ListSearch, ListSearchDebug, ListTagFilter, ListSearchSummary} from '../components/list';
import {notify, getAnonymousUserPermission, formatTime, anonUsername, parsePermissions, log, t} from '../utils';
import InlineEdit from 'react-inline-edit';

var extendCollectionToStateMixin = {
  componentDidMount () {
    this.listenTo(stores.collectionAssets, this.collectionLoaded);
    var uid, params = this.props.params;
    if (params && (uid=params.uid) && uid[0] === 'c') {
      actions.resources.readCollection({uid: uid})
      this.setState({
        collectionLoading: 1,
      })
    }
  },
  collectionLoaded (coll, uid) {
    this.setState({
      collection: coll,
      collectionLoading: 0,
    })
  },
  getInitialState () {
    return {
      collection: {
        url: false,
      },
      collectionLoading: -1,
      collectionUrl: `/collections/${this.props.params.uid}/`
    }
  },
}

var CollectionLanding = React.createClass({
  mixins: [
    extendCollectionToStateMixin,
    // mixins.collectionList,
    mixins.droppable,
    mixins.clickAssets,
    Navigation,
    Reflux.ListenerMixin,
    Reflux.connect(stores.selectedAsset),
  ],
  statics: {
    willTransitionTo: function(transition, params, idk, callback) {
      stores.pageState.setHeaderTitle(t('Collections'));
      stores.pageState.setAssetNavPresent(false);
      callback();
    }
  },
  dropAction ({file, event}) {
    actions.resources.createAsset({
      base64Encoded: event.target.result,
      name: file.name,
      lastModified: file.lastModified,
      parent: this.state.collectionUrl,
      contentType: file.type
    });
  },
  createCollection () {
    dataInterface.createCollection({
      name: prompt('collection name?'),
      parent: this.state.collectionUrl,
    }).done((data) => {
      this.redirect(`/collections/${data.uid}/`);
    })
  },
  changeCollectionName (evt) {
    var name = evt.target.value;
    if (this.state.collectionNamingRequest) {
      this.state.collectionNamingRequest.abort();
    }
    var req = dataInterface.patchCollection(this.props.params.uid, {
      name: name
    }).done((coll) => {
      this.setState({
        collectionNamingRequest: false,
        collectionNameSaving: false,
        collection: coll,
      });
    });
    this.setState({
      collectionNamingRequest: req,
      collectionNameSaving: true,
      collectionNaming: name,
    });
  },
  render () {
    var s = this.state,
        collectionName = s.collectionNameSaving ? s.collectionNaming : s.collection.name,
        collectionIdentifier = s.collection.name;

    if (s.collectionLoading) {
      return (
          <ui.Panel>
            {t('collection loading...')}
          </ui.Panel>
        );
    } else if (!s.collection.url) {
      return (
          <ui.Panel>
            {t('collection not loaded')}
          </ui.Panel>
        );
    }
    return (
      <ui.Panel>
        <bem.CollectionHeader__item m={'name'}>
          <bem.CollectionHeader__iconwrap><i /></bem.CollectionHeader__iconwrap>
          <bem.CollectionHeader__input
            m={{
                saving: s.collectionNameSaving
              }}
            value={collectionName}
            onChange={this.changeCollectionName}
            placeholder={t('collection name')}
            />
        </bem.CollectionHeader__item>
        <bem.CollectionNav>
          <bem.CollectionNav__actions className="k-form-list-actions">
            <button id="demo-menu-top-right"
                    className="mdl-button mdl-js-button mdl-button--fab mdl-button--colored">
              <i className="material-icons">add</i>
            </button>

            <ul className="mdl-menu mdl-menu--top-right mdl-js-menu mdl-js-ripple-effect"
                htmlFor="demo-menu-top-right">
                <bem.CollectionNav__button m={['new', 'new-collection']} className="mdl-menu__item"
                    onClick={this.createCollection}>
                  <i />
                  {t('new collection inside "___"').replace('___', collectionIdentifier)}
                </bem.CollectionNav__button>
              <li className="mdl-menu__item">
                <Dropzone onDropFiles={this.dropFiles} params={{destination: false}} fileInput>
                  <bem.CollectionNav__button m={['upload', 'upload-block']}>
                    <i className='fa fa-icon fa-cloud fa-fw' />
                    {t('upload into "___"').replace('___', collectionIdentifier)}
                  </bem.CollectionNav__button>
                </Dropzone>
              </li>
            </ul>
          </bem.CollectionNav__actions>
        </bem.CollectionNav>
        {this.renderCollectionList()}
      </ui.Panel>
      );
  },
  renderAssetRow (resource) {
    var currentUsername = stores.session.currentAccount && stores.session.currentAccount.username;
    var perm = parsePermissions(resource.owner, resource.permissions)
    var isSelected = this.state.selectedAssetUid === resource.uid;
    return <AssetRow key={resource.uid}
                      currentUsername={currentUsername}
                      perm={perm}
                      onActionButtonClick={this.onActionButtonClick}
                      isSelected={isSelected}
                      {...resource}
                        />
  },
  renderCollectionList () {
    var s = this.state,
        p = this.props;
    if (s.collectionLoading) {
      return (
        <bem.CollectionAssetList>
          <bem.CollectionAssetList__message m={'loading'}>
            {t('loading...')}
          </bem.CollectionAssetList__message>
        </bem.CollectionAssetList>
      );
    } else if (s.collection.url) {
      if (s.collection.children.count === 0) {
        return (
          <bem.CollectionAssetList>
            <bem.CollectionAssetList__message m={'loading'}>
              {t('no assets to display')}
            </bem.CollectionAssetList__message>
          </bem.CollectionAssetList>
        );
      }
      return (
        <bem.CollectionAssetList>
          {s.collection.children.results.map(this.renderAssetRow)}
        </bem.CollectionAssetList>
      );

      return (
        <bem.CollectionAssetList>
          {s.collectionList.map(this.renderAssetRow)}
        </bem.CollectionAssetList>
      );
    }
  },
});

export default CollectionLanding;
