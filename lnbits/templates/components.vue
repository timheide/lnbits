<template id="lnbits-wallet-list">
  <q-list
    v-if="g.user && g.user.wallets.length"
    dense
    class="lnbits-drawer__q-list"
  >
    <q-item
      v-for="walletRec in g.user.wallets"
      :key="walletRec.id"
      clickable
      :active="g.wallet && g.wallet.id === walletRec.id"
      @click="selectWallet(walletRec)"
    >
      <q-item-section side>
        <q-avatar
          size="md"
          :color="
            g.wallet && g.wallet.id === walletRec.id
              ? $q.dark.isActive
                ? 'primary'
                : 'primary'
              : 'grey-5'
          "
        >
          <q-icon
            name="flash_on"
            :size="$q.dark.isActive ? '21px' : '20px'"
            :color="$q.dark.isActive ? 'blue-grey-10' : 'grey-3'"
          ></q-icon>
        </q-avatar>
      </q-item-section>
      <q-item-section>
        <q-item-label lines="1"
          ><span v-text="walletRec.name"></span
        ></q-item-label>
        <q-item-label v-if="LNBITS_DENOMINATION != 'sats'" caption>
          <span
            v-text="
              parseFloat(String(walletRec.fsat).replaceAll(',', '')) / 100
            "
          ></span
          >&nbsp;
          <span v-text="LNBITS_DENOMINATION"></span>
        </q-item-label>
        <q-item-label v-else caption>
          <span v-text="walletRec.fsat"></span>&nbsp;
          <span v-text="LNBITS_DENOMINATION"></span>
        </q-item-label>
      </q-item-section>
      <q-item-section side v-show="g.wallet && g.wallet.id === walletRec.id">
      </q-item-section>
    </q-item>
    <q-item clickable @click="showForm = !showForm">
      <q-item-section side>
        <q-icon
          :name="showForm ? 'remove' : 'add'"
          color="grey-5"
          size="md"
        ></q-icon>
      </q-item-section>
      <q-item-section>
        <q-item-label
          lines="1"
          class="text-caption"
          v-text="$t('add_wallet')"
        ></q-item-label>
      </q-item-section>
    </q-item>
    <q-item v-if="showForm">
      <q-item-section>
        <q-form @submit="createWallet">
          <q-input filled dense v-model="walletName" label="Name wallet *">
            <template v-slot:append>
              <q-btn
                round
                dense
                flat
                icon="send"
                size="sm"
                @click="createWallet"
                :disable="walletName === ''"
              ></q-btn>
            </template>
          </q-input>
        </q-form>
      </q-item-section>
    </q-item>
  </q-list>
</template>

<template id="lnbits-extension-list">
  <q-list
    v-if="
      (g.user && userExtensions && userExtensions.length > 0) || !!searchTerm
    "
    dense
    class="lnbits-drawer__q-list"
  >
    <q-item>
      <q-item-section>
        <q-input
          v-model="searchTerm"
          dense
          borderless
          :label="$t('extensions')"
        >
        </q-input>
      </q-item-section>
    </q-item>
    <q-item
      v-for="extension in userExtensions"
      :key="extension.code"
      clickable
      :active="extension.isActive"
      tag="a"
      :href="extension.url"
    >
      <q-item-section side>
        <q-avatar size="md">
          <q-img :src="extension.tile" style="max-width: 20px"></q-img>
        </q-avatar>
      </q-item-section>
      <q-item-section>
        <q-item-label lines="1"
          ><span v-text="extension.name"></span>
        </q-item-label>
      </q-item-section>
      <q-item-section side v-show="extension.isActive">
        <q-icon name="chevron_right" color="grey-5" size="md"></q-icon>
      </q-item-section>
    </q-item>
    <div class="lt-md q-mt-xl q-mb-xl"></div>
  </q-list>
</template>

<template id="lnbits-manage">
  <q-list v-if="g.user" dense class="lnbits-drawer__q-list">
    <q-item-label header v-text="$t('manage')"></q-item-label>
    <div v-if="g.user.admin">
      <q-item v-if="showAdmin" to="/admin">
        <q-item-section side>
          <q-icon
            name="admin_panel_settings"
            :color="isActive('/admin') ? 'primary' : 'grey-5'"
            size="md"
          ></q-icon>
        </q-item-section>
        <q-item-section>
          <q-item-label lines="1" v-text="$t('server')"></q-item-label>
        </q-item-section>
      </q-item>
      <q-item v-if="showNode" to="/node">
        <q-item-section side>
          <q-icon
            name="developer_board"
            :color="isActive('/node') ? 'primary' : 'grey-5'"
            size="md"
          ></q-icon>
        </q-item-section>
        <q-item-section>
          <q-item-label lines="1" v-text="$t('node')"></q-item-label>
        </q-item-section>
      </q-item>
      <q-item v-if="showUsers" to="/users">
        <q-item-section side>
          <q-icon
            name="groups"
            :color="isActive('/users') ? 'primary' : 'grey-5'"
            size="md"
          ></q-icon>
        </q-item-section>
        <q-item-section>
          <q-item-label lines="1" v-text="$t('users')"></q-item-label>
        </q-item-section>
      </q-item>
      <q-item v-if="showAudit" to="/audit">
        <q-item-section side>
          <q-icon
            name="playlist_add_check_circle"
            :color="isActive('/audit') ? 'primary' : 'grey-5'"
            size="md"
          ></q-icon>
        </q-item-section>
        <q-item-section>
          <q-item-label lines="1" v-text="$t('audit')"></q-item-label>
        </q-item-section>
      </q-item>
    </div>
    <q-item v-if="showExtensions" to="/extensions">
      <q-item-section side>
        <q-icon
          name="extension"
          :color="isActive('/extensions') ? 'primary' : 'grey-5'"
          size="md"
        ></q-icon>
      </q-item-section>
      <q-item-section>
        <q-item-label lines="1" v-text="$t('extensions')"></q-item-label>
      </q-item-section>
    </q-item>
  </q-list>
</template>

<template id="lnbits-payment-details">
  <q-list separator>
    <q-item v-if="payment.tag">
      <q-item-section>
        <q-item-label v-text="$t('created')"></q-item-label>
        <q-item-label caption v-text="payment.date"></q-item-label>
      </q-item-section>

      <q-item-section side top>
        <q-item-label caption v-text="payment.dateFrom"></q-item-label>
      </q-item-section>
    </q-item>
    <q-item v-if="payment.expirydate">
      <q-item-section>
        <q-item-label v-text="$t('expiry')"></q-item-label>
        <q-item-label caption v-text="payment.expirydate"></q-item-label>
      </q-item-section>

      <q-item-section side top>
        <q-item-label caption v-text="payment.expirydateFrom"></q-item-label>
      </q-item-section>
    </q-item>
    <q-item>
      <q-item-section>
        <q-item-label v-text="$t('amount')"></q-item-label>
        <q-item-label caption>
          <span v-text="(payment.amount / 1000).toFixed(3)"></span>
          <span v-text="LNBITS_DENOMINATION"></span>
        </q-item-label>
      </q-item-section>
    </q-item>
    <q-item>
      <q-item-section>
        <q-item-label v-text="$t('fee')"></q-item-label>
        <q-item-label caption>
          <span v-text="(payment.fee / 1000).toFixed(3)"></span>
          <span v-text="LNBITS_DENOMINATION"></span>
        </q-item-label>
      </q-item-section>
    </q-item>
    <q-item>
      <q-item-section>
        <q-item-label v-text="$t('payment_hash')"></q-item-label>
        <q-item-label
          caption
          v-text="
            `${payment.payment_hash.slice(0, 12)}...${payment.payment_hash.slice(-12)}`
          "
        ></q-item-label>
      </q-item-section>
      <q-item-section side>
        <q-item-label>
          <q-icon
            name="content_copy"
            @click="copyText(payment.payment_hash)"
            size="1em"
            color="grey"
            class="cursor-pointer"
          />
        </q-item-label>
        <q-tooltip>
          <span v-text="payment.payment_hash"></span>
        </q-tooltip>
      </q-item-section>
    </q-item>
    <q-item>
      <q-item-section>
        <q-item-label v-text="$t('Invoice')"></q-item-label>
        <q-item-label
          caption
          v-text="
            `${payment.bolt11.slice(0, 12)}...${payment.bolt11.slice(-12)}`
          "
        ></q-item-label>
      </q-item-section>
      <q-item-section side>
        <q-item-label>
          <q-icon
            name="content_copy"
            @click="copyText(payment.bolt11)"
            size="1em"
            color="grey"
            class="cursor-pointer"
          />
        </q-item-label>
        <q-tooltip>
          <span v-text="payment.bolt11"></span>
        </q-tooltip>
      </q-item-section>
    </q-item>
    <q-item>
      <q-item-section>
        <q-item-label v-text="$t('memo')"></q-item-label>
        <q-item-label caption v-text="payment.memo"></q-item-label>
      </q-item-section>
    </q-item>
    <q-item v-if="payment.webhook">
      <q-item-section>
        <q-item-label v-text="$t('webhook')"></q-item-label>
        <q-item-label caption v-text="payment.webhook"></q-item-label>
      </q-item-section>
      <q-item-section side top>
        <q-item-label caption>
          <q-badge
            :color="webhookStatusColor"
            text-color="white"
            v-text="webhookStatusText"
          ></q-badge>
        </q-item-label>
      </q-item-section>
    </q-item>
    <q-item v-if="payment.preimage">
      <q-item-section>
        <q-item-label v-text="$t('payment_proof')"></q-item-label>
        <q-item-label caption v-text="payment.preimage"></q-item-label>
      </q-item-section>
    </q-item>

    <q-expansion-item
      expand-separator
      icon="info"
      header-class="text-grey-4"
      label="Extras"
      v-if="extras.length"
    >
      <template v-for="entry in extras">
        <q-item v-if="!!entry.value" key="entry.key" class="text-grey-4">
          <q-item-section>
            <q-item-label v-text="entry.key"></q-item-label>
            <q-item-label caption v-text="entry.value"></q-item-label>
          </q-item-section>
        </q-item>
      </template>
    </q-expansion-item>
  </q-list>
</template>

<template id="lnbits-dynamic-fields">
  <div v-if="formData">
    <div class="row q-mb-lg" v-for="o in options">
      <div class="col auto-width">
        <p v-if="o.options?.length" class="q-ml-xl">
          <span v-text="o.label || o.name"></span>
          <small v-if="o.description">
            (<span v-text="o.description"></span>)</small
          >
        </p>
        <lnbits-dynamic-fields
          v-if="o.options?.length"
          :options="o.options"
          v-model="formData[o.name]"
          @update:model-value="handleValueChanged"
          class="q-ml-xl"
        >
        </lnbits-dynamic-fields>
        <div v-else>
          <q-input
            v-if="o.type === 'number'"
            type="number"
            v-model="formData[o.name]"
            @update:model-value="handleValueChanged"
            :label="o.label || o.name"
            :hint="o.description"
            :rules="applyRules(o.required)"
            filled
            dense
          ></q-input>
          <q-input
            v-else-if="o.type === 'text'"
            type="textarea"
            rows="5"
            v-model="formData[o.name]"
            @update:model-value="handleValueChanged"
            :label="o.label || o.name"
            :hint="o.description"
            :rules="applyRules(o.required)"
            filled
            dense
          ></q-input>
          <q-input
            v-else-if="o.type === 'password'"
            v-model="formData[o.name]"
            @update:model-value="handleValueChanged"
            type="password"
            :label="o.label || o.name"
            :hint="o.description"
            :rules="applyRules(o.required)"
            filled
            dense
          ></q-input>
          <q-select
            v-else-if="o.type === 'select'"
            v-model="formData[o.name]"
            @update:model-value="handleValueChanged"
            :label="o.label || o.name"
            :hint="o.description"
            :options="o.values"
            :rules="applyRules(o.required)"
          ></q-select>
          <q-select
            v-else-if="o.isList"
            v-model.trim="formData[o.name]"
            @update:model-value="handleValueChanged"
            input-debounce="0"
            new-value-mode="add-unique"
            :label="o.label || o.name"
            :hint="o.description"
            :rules="applyRules(o.required)"
            filled
            multiple
            dense
            use-input
            use-chips
            multiple
            hide-dropdown-icon
          ></q-select>
          <div v-else-if="o.type === 'bool'">
            <q-item tag="label" v-ripple>
              <q-item-section avatar top>
                <q-checkbox
                  v-model="formData[o.name]"
                  @update:model-value="handleValueChanged"
                />
              </q-item-section>
              <q-item-section>
                <q-item-label
                  ><span v-text="o.label || o.name"></span
                ></q-item-label>
                <q-item-label caption>
                  <span v-text="o.description"></span>
                </q-item-label>
              </q-item-section>
            </q-item>
          </div>
          <q-input
            v-else-if="o.type === 'hidden'"
            v-model="formData[o.name]"
            type="text"
            style="display: none"
            :rules="applyRules(o.required)"
          ></q-input>
          <div v-else-if="o.type === 'chips'">
            <lnbits-dynamic-chips
              v-model="formData[o.name]"
              @update:model-value="handleValueChanged"
            ></lnbits-dynamic-chips>
          </div>
          <q-input
            v-else
            v-model="formData[o.name]"
            @update:model-value="handleValueChanged"
            :hint="o.description"
            :label="o.label || o.name"
            :rules="applyRules(o.required)"
            filled
            dense
          ></q-input>
        </div>
      </div>
    </div>
  </div>
</template>

<template id="lnbits-dynamic-chips">
  <q-input
    filled
    v-model="chip"
    @keydown.enter.prevent="addChip"
    type="text"
    label="wss://...."
    hint="Add relays"
    class="q-mb-md"
  >
    <q-btn @click="addChip" dense flat icon="add"></q-btn>
  </q-input>
  <div>
    <q-chip
      v-for="(chip, i) in chips"
      :key="chip"
      removable
      @remove="removeChip(i)"
      color="primary"
      text-color="white"
      :label="chip"
    >
    </q-chip>
  </div>
</template>

<template id="lnbits-notifications-btn">
  <q-btn
    v-if="g.user.wallets"
    :disabled="!this.isSupported"
    dense
    flat
    round
    @click="toggleNotifications()"
    :icon="this.isSubscribed ? 'notifications_active' : 'notifications_off'"
    size="sm"
    type="a"
  >
    <q-tooltip v-if="this.isSupported && !this.isSubscribed"
      >Subscribe to notifications</q-tooltip
    >
    <q-tooltip v-if="this.isSupported && this.isSubscribed"
      >Unsubscribe from notifications</q-tooltip
    >
    <q-tooltip v-if="this.isSupported && this.isPermissionDenied">
      Notifications are disabled,<br />please enable or reset permissions
    </q-tooltip>
    <q-tooltip v-if="!this.isSupported"
      >Notifications are not supported</q-tooltip
    >
  </q-btn>
</template>

<template id="lnbits-update-balance">
  <q-btn
    v-if="admin && small_btn"
    flat
    round
    color="primary"
    size="sm"
    icon="add"
  >
    <q-popup-edit class="bg-accent text-white" v-slot="scope" v-model="credit">
      <q-input
        filled
        :label="$t('credit_label', {denomination: denomination})"
        v-model="scope.value"
        dense
        autofocus
        @keyup.enter="updateBalance(scope)"
      >
        <template v-slot:append>
          <q-icon name="edit" />
        </template>
      </q-input>
    </q-popup-edit>
    <q-tooltip v-text="$t('credit_hint')"></q-tooltip>
  </q-btn>

  <q-btn
    v-if="admin && !small_btn"
    color="primary"
    :label="$t('credit_debit')"
    class="float-right q-mt-sm"
    size="sm"
  >
    <q-popup-edit class="bg-accent text-white" v-slot="scope" v-model="credit">
      <q-input
        filled
        :label="$t('credit_label', {denomination: denomination})"
        v-model="scope.value"
        dense
        autofocus
        @keyup.enter="updateBalance(scope)"
      >
        <template v-slot:append>
          <q-icon name="edit" />
        </template>
      </q-input>
    </q-popup-edit>
    <q-tooltip v-text="$t('credit_hint')"></q-tooltip>
  </q-btn>
</template>

<template id="lnbits-qrcode">
  <div class="qrcode__wrapper">
    <qrcode-vue
      :value="value"
      level="Q"
      render-as="svg"
      :margin="custom.margin"
      :size="custom.width"
      class="rounded-borders"
    ></qrcode-vue>
    <img
      v-if="custom.logo"
      class="qrcode__image"
      :src="custom.logo"
      alt="qrcode icon"
    />
  </div>
</template>

<template id="lnbits-lnurlpay-success-action">
  <div>
    <p
      class="q-mb-sm"
      v-text="success_action.message || success_action.description"
    ></p>
    <code
      v-if="decryptedValue"
      class="text-h6 q-mt-sm q-mb-none"
      v-text="decryptedValue"
    ></code>
    <p v-else-if="success_action.url" class="text-h6 q-mt-sm q-mb-none">
      <a
        target="_blank"
        style="color: inherit"
        :href="success_action.url"
        v-text="success_action.url"
      ></a>
    </p>
  </div>
</template>

<template id="payment-list">
  <div class="row items-center no-wrap">
    <div class="col" v-if="!mobileSimple || $q.screen.gt.sm">
      <q-input
        :label="$t('search_by_tag_memo_amount')"
        dense
        class="q-pr-xl"
        v-model="paymentsTable.search"
      >
        <template v-slot:before>
          <q-icon name="search"> </q-icon>
        </template>
        <template v-slot:append>
          <q-icon
            v-if="paymentsTable.search !== ''"
            name="close"
            @click="paymentsTable.search = ''"
            class="cursor-pointer"
          >
          </q-icon>
        </template>
      </q-input>
    </div>
    <div class="gt-sm col-auto">
      <q-btn-dropdown
        outline
        persistent
        class="q-mr-sm"
        color="grey"
        label="Export"
        split
        @click="exportCSV(false)"
      >
        <q-list>
          <q-item>
            <q-item-section>
              <q-input
                @keydown.enter="addFilterTag"
                filled
                dense
                v-model="exportTagName"
                type="text"
                label="Payment Tags"
                class="q-pa-sm"
              >
                <q-btn @click="addFilterTag" dense flat icon="add"></q-btn>
              </q-input>
            </q-item-section>
          </q-item>
          <q-item v-if="exportPaymentTagList.length">
            <q-item-section>
              <div>
                <q-chip
                  v-for="tag in exportPaymentTagList"
                  :key="tag"
                  removable
                  @remove="removeExportTag(tag)"
                  color="primary"
                  text-color="white"
                  :label="tag"
                ></q-chip>
              </div>
            </q-item-section>
          </q-item>

          <q-item>
            <q-item-section>
              <q-btn
                v-close-popup
                outline
                color="grey"
                @click="exportCSV(true)"
                label="Export to CSV with details"
              ></q-btn>
            </q-item-section>
          </q-item>
        </q-list>
      </q-btn-dropdown>
      <payment-chart :wallet="wallet"></payment-chart>
      <q-checkbox
        v-model="failedPaymentsToggle"
        checked-icon="warning"
        unchecked-icon="warning_off"
        :color="failedPaymentsToggle ? 'yellow' : 'grey'"
        size="xs"
      >
        <q-tooltip>
          <span v-text="`View failed payments`"></span>
        </q-tooltip>
      </q-checkbox>
    </div>
  </div>
  <div class="row q-my-md"></div>
  <q-table
    dense
    flat
    :rows="paymentsOmitter"
    :row-key="paymentTableRowKey"
    :columns="paymentsTable.columns"
    :no-data-label="$t('no_transactions')"
    :filter="paymentsTable.search"
    :loading="paymentsTable.loading"
    :hide-header="mobileSimple"
    :hide-bottom="mobileSimple"
    v-model:pagination="paymentsTable.pagination"
    @request="fetchPayments"
  >
    <template v-slot:header="props">
      <q-tr :props="props" class="text-grey-5">
        <q-th auto-width></q-th>
        <q-th
          v-for="col in props.cols"
          :key="col.name"
          :props="props"
          v-text="col.label"
        ></q-th>
      </q-tr>
    </template>
    <template v-slot:body="props">
      <q-tr :props="props">
        <q-td auto-width class="text-center">
          <q-icon
            v-if="props.row.isPaid"
            size="14px"
            :name="props.row.isOut ? 'call_made' : 'call_received'"
            :color="props.row.isOut ? 'pink' : 'green'"
            @click="props.expand = !props.expand"
          ></q-icon>
          <q-icon
            v-else-if="props.row.isFailed"
            name="warning"
            color="yellow"
            @click="props.expand = !props.expand"
          >
            <q-tooltip><span>failed</span></q-tooltip>
          </q-icon>
          <q-icon
            v-else
            name="settings_ethernet"
            color="grey"
            @click="props.expand = !props.expand"
          >
            <q-tooltip><span v-text="$t('pending')"></span></q-tooltip>
          </q-icon>
        </q-td>
        <q-td
          key="time"
          :props="props"
          style="white-space: normal; word-break: break-all"
        >
          <q-badge v-if="props.row.tag" color="yellow" text-color="black">
            <a
              v-text="'#' + props.row.tag"
              class="inherit"
              :href="['/', props.row.tag].join('')"
            ></a>
          </q-badge>
          <span class="q-ml-sm" v-text="props.row.memo"></span>
          <br />

          <i>
            <span class="text-grey-5" v-text="props.row.dateFrom"></span>
            <q-tooltip><span v-text="props.row.date"></span></q-tooltip>
          </i>
        </q-td>
        <q-td
          auto-width
          key="amount"
          v-if="denomination != 'sats'"
          :props="props"
          class="col1"
          v-text="parseFloat(String(props.row.fsat).replaceAll(',', '')) / 100"
        >
        </q-td>
        <q-td class="col2" auto-width key="amount" v-else :props="props">
          <span v-text="props.row.fsat"></span>
          <br />
          <i v-if="props.row.extra.wallet_fiat_currency">
            <span
              v-text="
                formatCurrency(
                  props.row.extra.wallet_fiat_amount,
                  props.row.extra.wallet_fiat_currency
                )
              "
            ></span>
            <br />
          </i>
          <i v-if="props.row.extra.fiat_currency">
            <span
              v-text="
                formatCurrency(
                  props.row.extra.fiat_amount,
                  props.row.extra.fiat_currency
                )
              "
            ></span>
          </i>
        </q-td>
        <q-dialog v-model="props.expand" :props="props" position="top">
          <q-card class="q-pa-sm q-pt-xl lnbits__dialog-card">
            <q-card-section class="">
              <q-list bordered separator>
                <q-expansion-item
                  expand-separator
                  :default-opened="!(props.row.isIn && props.row.isPending)"
                >
                  <template v-slot:header>
                    <q-item-section avatar>
                      <q-icon
                        :color="
                          props.row.isPaid && props.row.isIn
                            ? 'green'
                            : props.row.isPaid && props.row.isOut
                              ? 'pink'
                              : props.row.isFailed
                                ? 'yellow'
                                : 'grey'
                        "
                        :name="
                          props.row.isPaid && props.row.isIn
                            ? 'call_received'
                            : props.row.isPaid && props.row.isOut
                              ? 'call_made'
                              : props.row.isFailed
                                ? 'warning'
                                : 'settings_ethernet'
                        "
                      />
                    </q-item-section>

                    <q-item-section>
                      <q-item-label
                        v-text="
                          props.row.isIn && props.row.isPending
                            ? $t('invoice_waiting')
                            : props.row.isOut && props.row.isPending
                              ? $t('outgoing_payment_pending')
                              : props.row.isPaid && props.row.isIn
                                ? $t('payment_received')
                                : props.row.isPaid && props.row.isOut
                                  ? $t('payment_sent')
                                  : props.row.isFailed
                                    ? $t('payment_failed')
                                    : ''
                        "
                      ></q-item-label>
                    </q-item-section>
                    <q-item-section v-if="props.row.tag" side>
                      <q-badge
                        v-if="props.row.extra && !!props.row.extra.tag"
                        color="yellow"
                        text-color="black"
                      >
                        #<span v-text="props.row.tag"></span>
                      </q-badge>
                    </q-item-section>
                  </template>
                  <q-separator></q-separator>
                  <lnbits-payment-details
                    :payment="props.row"
                  ></lnbits-payment-details>
                </q-expansion-item>
              </q-list>
              <div
                v-if="props.row.isIn && props.row.isPending && props.row.bolt11"
                class="text-center q-my-lg"
              >
                <a :href="'lightning:' + props.row.bolt11">
                  <lnbits-qrcode
                    :value="'lightning:' + props.row.bolt11.toUpperCase()"
                  ></lnbits-qrcode>
                </a>
              </div>
            </q-card-section>
            <q-card-section>
              <div class="row">
                <q-btn
                  v-if="
                    props.row.isIn && props.row.isPending && props.row.bolt11
                  "
                  outline
                  color="grey"
                  @click="copyText(props.row.bolt11)"
                  :label="$t('copy_invoice')"
                ></q-btn>
                <q-btn
                  v-close-popup
                  flat
                  color="grey"
                  class="q-ml-auto"
                  :label="$t('close')"
                ></q-btn>
              </div>
            </q-card-section>
          </q-card>
        </q-dialog>
      </q-tr>
    </template>
  </q-table>
</template>

<template id="lnbits-extension-rating">
  <div style="margin-bottom: 3px">
    <q-rating v-model="rating" size="1.5em" :max="5" color="primary"
      ><q-tooltip>
        <span v-text="$t('extension_rating_soon')"></span> </q-tooltip
    ></q-rating>
  </div>
</template>

<template id="lnbits-extension-settings-form">
  <q-form v-if="settings" @submit="updateSettings" class="q-gutter-md">
    <lnbits-dynamic-fields
      :options="options"
      v-model="settings"
    ></lnbits-dynamic-fields>
    <div class="row q-mt-lg">
      <q-btn v-close-popup unelevated color="primary" type="submit"
        >Update</q-btn
      >
      <q-btn v-close-popup unelevated color="danger" @click="resetSettings"
        >Reset</q-btn
      >
      <slot name="actions"></slot>
    </div>
  </q-form>
</template>

<template id="lnbits-extension-settings-btn-dialog">
  <q-btn
    v-if="options"
    unelevated
    @click="show = true"
    color="primary"
    icon="settings"
    class="float-right"
  >
    <q-dialog v-model="show" position="top">
      <q-card class="q-pa-lg q-pt-xl lnbits__dialog-card">
        <lnbits-extension-settings-form
          :options="options"
          :adminkey="adminkey"
          :endpoint="endpoint"
        >
          <template v-slot:actions>
            <q-btn v-close-popup flat color="grey" class="q-ml-auto"
              >Close</q-btn
            >
          </template>
        </lnbits-extension-settings-form>
      </q-card>
    </q-dialog>
  </q-btn>
</template>

<template id="lnbits-funding-sources">
  <div class="funding-sources">
    <h6 class="q-mt-xl q-mb-md">Funding Sources</h6>
    <div class="row">
      <div class="col-12">
        <p>Active Funding<small> (Requires server restart)</small></p>
        <q-select
          filled
          v-model="formData.lnbits_backend_wallet_class"
          hint="Select the active funding wallet"
          :options="sortedAllowedFundingSources"
          :option-label="item => getFundingSourceLabel(item)"
        ></q-select>
      </div>
    </div>
    <q-list
      class="q-mt-md"
      v-for="(fund, idx) in allowedFundingSources"
      :key="idx"
    >
      <div
        v-if="
          fundingSources.get(fund) &&
          fund === formData.lnbits_backend_wallet_class
        "
      >
        <div
          class="row"
          v-for="([key, prop], i) in Object.entries(fundingSources.get(fund))"
          :key="i"
        >
          <div class="col-12">
            <q-input
              filled
              type="text"
              class="q-mt-sm"
              v-model="formData[key]"
              :label="prop.label"
              :hint="prop.hint"
            ></q-input>
          </div>
        </div>
      </div>
    </q-list>
  </div>
</template>

<template id="payment-chart">
  <span id="payment-chart">
    <q-btn dense flat round icon="show_chart" color="grey" @click="showChart">
      <q-tooltip>
        <span v-text="$t('chart_tooltip')"></span>
      </q-tooltip>
    </q-btn>

    <q-dialog v-model="paymentsChart.show" position="top">
      <q-card class="q-pa-sm" style="width: 800px; max-width: unset">
        <q-card-section>
          <div class="row q-gutter-sm justify-between">
            <div class="text-h6">Payments Chart</div>
            <q-select
              label="Group"
              filled
              dense
              v-model="paymentsChart.group"
              style="min-width: 120px"
              :options="paymentsChart.groupOptions"
            >
            </q-select>
          </div>
          <canvas ref="canvas" width="600" height="400"></canvas>
        </q-card-section>
      </q-card>
    </q-dialog>
  </span>
</template>
