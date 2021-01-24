import moment from 'moment';


export interface ScheduledJob {
    id: number,
    scheduled_at?: string,
    scheduled_for?: string
}

export interface Update {
    id: number,
    realm_type: string,
    realm_id: string,
    body: string,
    attachments: string,
    job: ScheduledJob
}

const schoologyTimestampFormat = 'YYYY-MM-DD HH:mm:ss';

export function schoologyTimeToMoment(schoologyTimestamp: string): moment.Moment {
    return moment(schoologyTimestamp, schoologyTimestampFormat);
}

export function momentToSchoologyTime(momentInstance: moment.Moment): string {
    return momentInstance.format(schoologyTimestampFormat);
}
