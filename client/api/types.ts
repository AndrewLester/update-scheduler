import moment from 'moment';


export interface ScheduledJob {
    id: string,
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

const schoologyTimestampFormat = 'YYYY-MM-DD HH:mm:ss';

export function schoologyTimeToMoment(schoologyTimestamp: string): moment.Moment {
    return moment(schoologyTimestamp, schoologyTimestampFormat);
}

export function momentToSchoologyTime(momentInstance: moment.Moment): string {
    return momentInstance.format(schoologyTimestampFormat);
}
