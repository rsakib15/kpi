// TODO: double check the display logic for buttons (permissions)

/**
 * This is intended to be displayed in multiple places:
 * - library asset landing page
 * - library listing row
 * - project landing page (TODO in future)
 * - projects listing row (TODO in future)
 */

import React from 'react';
import Reflux from 'reflux';
import autoBind from 'react-autobind';
import {hashHistory} from 'react-router';
import PropTypes from 'prop-types';
import reactMixin from 'react-mixin';
import ui from 'js/ui';
import {bem} from 'js/bem';
import {t} from 'js/utils';
import {actions} from 'js/actions';
import assetUtils from 'js/assetUtils';
import {ASSET_TYPES} from 'js/constants';
import mixins from 'js/mixins';
import ownedCollectionsStore from './ownedCollectionsStore';

const assetActions = mixins.clickAssets.click.asset;

/**
 * @prop {object} asset
 */
class AssetActionButtons extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      ownedCollections: ownedCollectionsStore.data.collections,
      shouldHidePopover: false,
      isPopoverVisible: false
    };
    autoBind(this);
  }

  componentDidMount() {
    this.listenTo(ownedCollectionsStore, this.onOwnedCollectionsStoreChanged);
  }

  onOwnedCollectionsStoreChanged(storeData) {
    this.setState({
      ownedCollections: storeData.collections
    });
  }

  // methods for inner workings of component

  onMouseLeave() {
    // force hide popover in next render cycle
    // (ui.PopoverMenu interface handles it this way)
    if (this.state.isPopoverVisible) {
      this.setState({shouldHidePopover: true});
    }
  }

  onPopoverSetVisible() {
    this.setState({isPopoverVisible: true});
  }

  // Methods for managing the asset

  modifyDetails() {
    assetUtils.modifyDetails(this.props.asset);
  }

  editLanguages() {
    assetUtils.editLanguages(this.props.asset);
  }

  share() {
    assetUtils.share(this.props.asset);
  }

  showTagsModal() {
    assetUtils.editTags(this.props.asset);
  }

  replace() {
    assetUtils.replaceForm(this.props.asset);
  }

  delete() {
    assetActions.delete(
      this.props.asset,
      assetUtils.getAssetDisplayName(this.props.asset).final,
      this.onDeleteComplete.bind(this, this.props.asset.uid)
    );
  }

  /**
   * Navigates out of nonexistent paths after asset was successfuly deleted
   */
  onDeleteComplete(assetUid) {
    if (this.isLibrarySingle() && this.currentAssetID() === assetUid) {
      hashHistory.push('/library');
    }
    if (this.isFormSingle() && this.currentAssetID() === assetUid) {
      hashHistory.push('/forms');
    }
  }

  deploy() {
    mixins.dmix.deployAsset(this.props.asset);
  }

  archive() {
    assetActions.archive(this.props.asset);
  }

  unarchive() {
    assetActions.unarchive(this.props.asset);
  }

  clone() {
    assetActions.clone(this.props.asset);
  }

  cloneAsSurvey() {
    assetActions.cloneAsSurvey(
      this.props.asset.uid,
      assetUtils.getAssetDisplayName(this.props.asset).final
    );
  }

  cloneAsTemplate() {
    assetActions.cloneAsTemplate(
      this.props.asset.uid,
      assetUtils.getAssetDisplayName(this.props.asset).final
    );
  }

  moveToCollection(collectionUrl) {
    actions.library.moveToCollection(this.props.asset.uid, collectionUrl);
  }

  subscribeToCollection() {
    actions.library.subscribeToCollection(this.props.asset.url);
  }

  unsubscribeFromCollection() {
    actions.library.unsubscribeFromCollection(this.props.asset.uid);
  }

  viewContainingCollection() {
    const parentArr = this.props.asset.parent.split('/');
    const parentAssetUid = parentArr[parentArr.length - 2];
    hashHistory.push(`/library/asset/${parentAssetUid}`);
  }

  render() {
    const assetType = this.props.asset ? this.props.asset.asset_type : null;
    const userCanEdit = true;
    const hasDetailsEditable = (
      assetType === ASSET_TYPES.template.id ||
      assetType === ASSET_TYPES.collection.id
    );
    const isDeployable = true;
    const downloads = [];
    const isUserSubscribed = assetUtils.isUserSubscribedToAsset(this.props.asset);
    const isSelfOwned = assetUtils.isSelfOwned(this.props.asset);
    const isPublic = assetUtils.isAssetPublic(this.props.asset.permissions);

    return (
      <bem.AssetActionButtons onMouseLeave={this.onMouseLeave}>
        {userCanEdit && assetType !== ASSET_TYPES.collection.id &&
          <bem.AssetActionButtons__iconButton
            href={`#/library/asset/${this.props.asset.uid}/edit`}
            data-tip={t('Edit in Form Builder')}
            className='right-tooltip'
          >
            <i className='k-icon k-icon-edit'/>
          </bem.AssetActionButtons__iconButton>
        }

        {userCanEdit && hasDetailsEditable &&
          <bem.AssetActionButtons__iconButton
            onClick={this.modifyDetails}
            data-tip={t('Modify details')}
            className='right-tooltip'
          >
            <i className='k-icon k-icon-settings' />
          </bem.AssetActionButtons__iconButton>
        }

        {userCanEdit &&
          <bem.AssetActionButtons__iconButton
            onClick={this.showTagsModal}
            data-tip= {t('Edit Tags')}
            className='right-tooltip'
          >
            <i className='k-icon k-icon-tag'/>
          </bem.AssetActionButtons__iconButton>
        }

        {userCanEdit &&
          <bem.AssetActionButtons__iconButton
            onClick={this.share}
            data-tip= {t('Share')}
            className='right-tooltip'
          >
            <i className='k-icon k-icon-user-share'/>
          </bem.AssetActionButtons__iconButton>
        }

        <bem.AssetActionButtons__iconButton
          onClick={this.clone}
          data-tip={t('Clone')}
          className='right-tooltip'
        >
          <i className='k-icon k-icon-clone'/>
        </bem.AssetActionButtons__iconButton>

        {userCanEdit && assetType === ASSET_TYPES.template.id &&
          <bem.AssetActionButtons__iconButton
            onClick={this.cloneAsSurvey}
            data-tip={t('Create project')}
            className='right-tooltip'
          >
            <i className='k-icon k-icon-projects'/>
          </bem.AssetActionButtons__iconButton>
        }

        {this.props.asset.parent !== null &&
          !this.props.asset.parent.includes(this.currentAssetID()) &&
          <bem.AssetActionButtons__iconButton
            onClick={this.viewContainingCollection}
            data-tip={t('View containing Collection')}
            className='right-tooltip'
          >
            <i className='k-icon k-icon-folder'/>
          </bem.AssetActionButtons__iconButton>
        }

        <ui.PopoverMenu
          triggerLabel={<i className='k-icon k-icon-more'/>}
          triggerTip={t('More Actions')}
          triggerClassName='right-tooltip'
          clearPopover={this.state.shouldHidePopover}
          popoverSetVisible={this.onPopoverSetVisible}
        >
          {userCanEdit && assetType === ASSET_TYPES.survey.id && isDeployable &&
            <bem.PopoverMenu__link onClick={this.deploy}>
              <i className='k-icon k-icon-deploy'/>
              {t('Deploy')}
            </bem.PopoverMenu__link>
          }

          {userCanEdit &&
            assetType === ASSET_TYPES.survey.id &&
            this.props.has_deployment &&
            !this.props.deployment__active &&
            <bem.PopoverMenu__link onClick={this.unarchive}>
              <i className='k-icon k-icon-archived'/>
              {t('Unarchive')}
            </bem.PopoverMenu__link>
          }

          {userCanEdit && assetType === ASSET_TYPES.survey.id &&
            <bem.PopoverMenu__link onClick={this.replace}>
              <i className='k-icon k-icon-replace'/>
              {t('Replace form')}
            </bem.PopoverMenu__link>
          }

          {userCanEdit && assetType !== ASSET_TYPES.collection.id &&
            <bem.PopoverMenu__link onClick={this.editLanguages}>
              <i className='k-icon k-icon-language'/>
              {t('Manage Translations')}
            </bem.PopoverMenu__link>
          }

          {downloads.map((dl) => {
            return (
              <bem.PopoverMenu__link
                href={dl.url}
                key={`dl-${dl.format}`}
              >
                <i className={`k-icon k-icon-${dl.format}-file`}/>
                {t('Download')}&nbsp;{dl.format.toString().toUpperCase()}
              </bem.PopoverMenu__link>
            );
          })}

          {!isUserSubscribed &&
            !isSelfOwned &&
            isPublic &&
            assetType === ASSET_TYPES.collection.id &&
            <bem.PopoverMenu__link onClick={this.subscribeToCollection}>
              <i className='k-icon k-icon-subscribe'/>
              {t('Subscribe')}
            </bem.PopoverMenu__link>
          }

          {isUserSubscribed &&
            !isSelfOwned &&
            isPublic &&
            assetType === ASSET_TYPES.collection.id &&
            <bem.PopoverMenu__link onClick={this.unsubscribeFromCollection}>
              <i className='k-icon k-icon-unsubscribe'/>
              {t('Unsubscribe')}
            </bem.PopoverMenu__link>
          }

          {userCanEdit &&
            assetType !== ASSET_TYPES.survey.id &&
            assetType !== ASSET_TYPES.collection.id &&
            this.props.asset.parent !== null &&
            <bem.PopoverMenu__link onClick={this.moveToCollection.bind(this, null)}>
              <i className='k-icon k-icon-folder-out'/>
              {t('Remove from collection')}
            </bem.PopoverMenu__link>
          }

          {userCanEdit &&
            assetType !== ASSET_TYPES.survey.id &&
            assetType !== ASSET_TYPES.collection.id &&
            this.state.ownedCollections.length > 0 && [
            <bem.PopoverMenu__heading key='heading'>
              {t('Move to')}
            </bem.PopoverMenu__heading>,
            <bem.PopoverMenu__moveTo key='list'>
              {this.state.ownedCollections.map((collection) => {
                const modifiers = ['move-coll-item'];
                const isAssetParent = collection.url === this.props.asset.parent;
                if (isAssetParent) {
                  modifiers.push('move-coll-item-parent');
                }
                return (
                  <bem.PopoverMenu__item
                    onClick={this.moveToCollection.bind(this, collection.url)}
                    key={collection.uid}
                    title={collection.name}
                    m={modifiers}
                  >
                    <i className='k-icon k-icon-folder-in'/>
                    {collection.name}
                  </bem.PopoverMenu__item>
                );
              })}
            </bem.PopoverMenu__moveTo>
          ]}

          {userCanEdit &&
            assetType === ASSET_TYPES.survey.id &&
            this.props.has_deployment &&
            this.props.deployment__active &&
            <bem.PopoverMenu__link onClick={this.archive}>
              <i className='k-icon k-icon-archived'/>
              {t('Archive')}
            </bem.PopoverMenu__link>
          }

          {userCanEdit && assetType === ASSET_TYPES.survey.id &&
            <bem.PopoverMenu__link onClick={this.cloneAsTemplate}>
              <i className='k-icon k-icon-template'/>
              {t('Create template')}
            </bem.PopoverMenu__link>
          }

          {userCanEdit &&
            <bem.PopoverMenu__link onClick={this.delete}>
              <i className='k-icon k-icon-trash'/>
              {t('Delete')}
            </bem.PopoverMenu__link>
          }
        </ui.PopoverMenu>
      </bem.AssetActionButtons>
    );
  }
}

reactMixin(AssetActionButtons.prototype, mixins.contextRouter);
reactMixin(AssetActionButtons.prototype, Reflux.ListenerMixin);
AssetActionButtons.contextTypes = {
  router: PropTypes.object
};

export default AssetActionButtons;