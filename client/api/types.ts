import moment from 'moment';


export interface ScheduledJob {
    id: string,
    scheduled_at?: string,
    scheduled_for?: string,
    scheduled_in?: string
}

export interface Update {
    id: number,
    realm_type: string,
    realm_id: string,
    body: string,
    attachments: string,
    job: ScheduledJob | null
}

export interface Realm {
    id: string,
    name: string,
    realm_type: string
}

export function isScheduled(update: Update): boolean {
    return update.job !== null && update.job.id !== '';
}

const schoologyTimestampFormat = 'YYYY-MM-DD HH:mm:ss';

export function schoologyTimeToMoment(schoologyTimestamp: string): moment.Moment {
    return moment(schoologyTimestamp, schoologyTimestampFormat);
}

export function momentToSchoologyTime(momentInstance: moment.Moment): string {
    return momentInstance.format(schoologyTimestampFormat);
}

export function getNewUpdate(): Update {
    return {
        id: -1,
        body: '',
        attachments: '',
        realm_id: '',
        realm_type: '',
        job: null,
    };
}
