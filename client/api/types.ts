import moment from 'moment';


export interface ScheduledJob {
    id: number,
    scheduled_at?: string,
    scheduled_for?: string
}

export interface Update {
    id: number,
    realm_type: string,
    realm_id: number,
    body: string,
    attachments: string,
    job: ScheduledJob | null
}

export interface Realm {
    id: string,
    name: string,
    realm_type: string
}

const schoologyTimestampFormat = 'YYYY-MM-DD HH:mm:ss';

export function schoologyTimeToMoment(schoologyTimestamp: string): moment.Moment {
    return moment(schoologyTimestamp, schoologyTimestampFormat);
}

export function momentToSchoologyTime(momentInstance: moment.Moment): string {
    return momentInstance.format(schoologyTimestampFormat);
}
