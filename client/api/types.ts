import moment from 'moment';

export interface ScheduledJob {
    id: string;
    scheduled_at?: string;
    scheduled_for?: string;
    scheduled_in?: string;
}

export interface Attachment {
    id: number;
    type: 'file' | 'link' | 'video';
    title?: string;
    url: string;
    image?: string;
    icon?: string;
    summary?: string;
}

export interface Update {
    id: number;
    body: string;
    job: ScheduledJob | null;
    attachments: Attachment[];
    realms: Realm[];
}

export interface ScheduledUpdate extends Update {
    job: ScheduledJob;
}

export interface Realm {
    id: string;
    name: string;
    type: string;
}

export function isScheduled(update: Update): update is ScheduledUpdate {
    return update.job !== null && update.job.id !== '';
}

export function getPostDate(update: Update): moment.Moment {
    if (!isScheduled(update)) {
        throw new Error('Unscheduled updates do not have a post date');
    }

    if (update.job.scheduled_for) {
        return schoologyTimeToMoment(update.job.scheduled_for);
    }

    return schoologyTimeToMoment(update.job.scheduled_at!).add(
        moment.duration(update.job.scheduled_in)
    );
}

export function scheduledSort(update1: Update, update2: Update): number {
    if (!isScheduled(update1) || !isScheduled(update2)) {
        throw new Error('Sorting of unscheduled updates is invalid');
    }

    const postDate1 = getPostDate(update1);
    const postDate2 = getPostDate(update2);

    return postDate1.valueOf() - postDate2.valueOf();
}

const schoologyTimestampFormat = 'YYYY-MM-DD HH:mm:ss';

export function schoologyTimeToMoment(
    schoologyTimestamp: string
): moment.Moment {
    return moment(schoologyTimestamp, schoologyTimestampFormat);
}

export function momentToSchoologyTime(momentInstance: moment.Moment): string {
    return momentInstance.format(schoologyTimestampFormat);
}

export function getNewUpdate(): Update {
    return {
        id: -1,
        body: '',
        attachments: [],
        realms: [],
        job: null,
    };
}
